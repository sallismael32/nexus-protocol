// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title NexusProofMarketplace
 * @notice Paid proof verification - customers pay ETH to verify proofs
 */
contract NexusProofMarketplace {
    
    address public owner;
    uint256 public pricePerProof;
    uint256 public totalRevenue;
    uint256 public totalProofsVerified;
    
    mapping(bytes32 => bool) public verifiedProofs;
    mapping(address => uint256) public customerProofCount;
    
    event ProofPurchased(address indexed customer, bytes32 indexed commitment, uint256 price, uint256 timestamp);
    event PriceUpdated(uint256 oldPrice, uint256 newPrice);
    event Withdrawal(address indexed to, uint256 amount);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    constructor(uint256 _pricePerProof) {
        owner = msg.sender;
        pricePerProof = _pricePerProof;
    }
    
    function purchaseVerification(
        bytes32 commitment,
        uint256 blockNumber,
        bytes32 blockHash,
        bytes32 leafHash,
        bytes32[] calldata merkleProof,
        bool[] calldata proofIsRight
    ) external payable returns (bool) {
        require(msg.value >= pricePerProof, "Insufficient payment");
        require(!verifiedProofs[commitment], "Already verified");
        
        require(_verifyMerkleProof(leafHash, merkleProof, proofIsRight, commitment), "Invalid proof");
        
        verifiedProofs[commitment] = true;
        customerProofCount[msg.sender]++;
        totalProofsVerified++;
        totalRevenue += msg.value;
        
        if (msg.value > pricePerProof) {
            payable(msg.sender).transfer(msg.value - pricePerProof);
        }
        
        emit ProofPurchased(msg.sender, commitment, pricePerProof, block.timestamp);
        return true;
    }
    
    function isVerified(bytes32 commitment) external view returns (bool) {
        return verifiedProofs[commitment];
    }
    
    function setPrice(uint256 newPrice) external onlyOwner {
        uint256 oldPrice = pricePerProof;
        pricePerProof = newPrice;
        emit PriceUpdated(oldPrice, newPrice);
    }
    
    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No balance");
        payable(owner).transfer(balance);
        emit Withdrawal(owner, balance);
    }
    
    function _verifyMerkleProof(
        bytes32 leaf,
        bytes32[] calldata proof,
        bool[] calldata isRight,
        bytes32 root
    ) internal pure returns (bool) {
        if (proof.length != isRight.length) return false;
        bytes32 computed = leaf;
        for (uint256 i = 0; i < proof.length; i++) {
            if (isRight[i]) {
                computed = keccak256(abi.encodePacked(computed, proof[i]));
            } else {
                computed = keccak256(abi.encodePacked(proof[i], computed));
            }
        }
        return computed == root;
    }
    
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
