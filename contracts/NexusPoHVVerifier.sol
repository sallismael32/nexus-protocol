// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title NexusPoHVVerifier
 * @notice On-chain verification of Proof of Historical Validity witnesses
 * @dev Fixed version - no stack too deep issues
 */
contract NexusPoHVVerifier {
    
    mapping(uint256 => bytes32) public blockHashes;
    mapping(uint256 => bytes32) public stateRoots;
    mapping(bytes32 => bool) public verifiedCommitments;
    
    event HeaderRegistered(uint256 indexed blockNumber, bytes32 blockHash);
    event WitnessVerified(bytes32 indexed commitment, uint256 blockNumber, address verifier);
    
    error HeaderNotRegistered();
    error HeaderMismatch();
    error InvalidMerkleProof();
    
    function registerHeader(
        uint256 blockNumber,
        bytes32 blockHash,
        bytes32 stateRoot
    ) external {
        blockHashes[blockNumber] = blockHash;
        stateRoots[blockNumber] = stateRoot;
        emit HeaderRegistered(blockNumber, blockHash);
    }
    
    function verifyWitness(
        bytes32 commitment,
        uint256 blockNumber,
        bytes32 claimedBlockHash,
        bytes32 leafHash,
        bytes32[] calldata merkleProof,
        bool[] calldata proofIsRight
    ) external returns (bool) {
        bytes32 registeredHash = blockHashes[blockNumber];
        if (registeredHash == bytes32(0)) revert HeaderNotRegistered();
        if (registeredHash != claimedBlockHash) revert HeaderMismatch();
        
        if (!_verifyProof(leafHash, merkleProof, proofIsRight, commitment)) {
            revert InvalidMerkleProof();
        }
        
        verifiedCommitments[commitment] = true;
        emit WitnessVerified(commitment, blockNumber, msg.sender);
        return true;
    }
    
    function verifyWitnessView(
        bytes32 commitment,
        uint256 blockNumber,
        bytes32 claimedBlockHash,
        bytes32 leafHash,
        bytes32[] calldata merkleProof,
        bool[] calldata proofIsRight
    ) external view returns (bool valid, string memory reason) {
        if (blockHashes[blockNumber] == bytes32(0)) {
            return (false, "Header not registered");
        }
        if (blockHashes[blockNumber] != claimedBlockHash) {
            return (false, "Header mismatch");
        }
        if (!_verifyProof(leafHash, merkleProof, proofIsRight, commitment)) {
            return (false, "Invalid Merkle proof");
        }
        return (true, "Valid");
    }
    
    function _verifyProof(
        bytes32 leaf,
        bytes32[] calldata proof,
        bool[] calldata isRight,
        bytes32 root
    ) internal pure returns (bool) {
        if (proof.length != isRight.length) return false;
        
        bytes32 computed = leaf;
        uint256 len = proof.length;
        
        for (uint256 i = 0; i < len;) {
            bytes32 sibling = proof[i];
            if (isRight[i]) {
                computed = _hashPair(computed, sibling);
            } else {
                computed = _hashPair(sibling, computed);
            }
            unchecked { ++i; }
        }
        
        return computed == root;
    }
    
    function _hashPair(bytes32 a, bytes32 b) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked(a, b));
    }
    
    function isVerified(bytes32 commitment) external view returns (bool) {
        return verifiedCommitments[commitment];
    }
    
    function getBlockHash(uint256 blockNumber) external view returns (bytes32) {
        return blockHashes[blockNumber];
    }
}
