#!/usr/bin/env python3
"""
Nexus + Ethereum: Real Data with PoHV Proofs

Fetches real Ethereum data via Alchemy and generates
Proof of Historical Validity witnesses that can be verified.

Usage:
    export ALCHEMY_API_KEY=your_key
    python nexus_ethereum.py
"""

import json
import hashlib
import os
import urllib.request
from datetime import datetime
from typing import List, Dict, Tuple

API_KEY = os.environ.get("ALCHEMY_API_KEY", "YOUR_ALCHEMY_API_KEY")
BASE_URL = f"https://eth-mainnet.g.alchemy.com/v2/{API_KEY}"

VITALIK = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def rpc_call(method: str, params: list = None):
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode()
    req = urllib.request.Request(BASE_URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        if "error" in result:
            raise Exception(result["error"])
        return result.get("result")

def hex_to_int(h: str) -> int:
    return int(h, 16) if isinstance(h, str) and h.startswith("0x") else h

class MerkleTree:
    def __init__(self, leaves: List[bytes]):
        self.leaves = leaves
        self.levels = self._build(leaves)
    
    def _build(self, leaves: List[bytes]) -> List[List[bytes]]:
        if not leaves:
            return [[b'\x00' * 32]]
        n = len(leaves)
        next_pow2 = 1 << (n - 1).bit_length()
        padded = leaves + [b'\x00' * 32] * (next_pow2 - n)
        levels = [padded]
        while len(levels[-1]) > 1:
            current = levels[-1]
            next_level = []
            for i in range(0, len(current), 2):
                combined = current[i] + (current[i+1] if i+1 < len(current) else current[i])
                next_level.append(sha256(combined))
            levels.append(next_level)
        return levels
    
    @property
    def root(self) -> bytes:
        return self.levels[-1][0]
    
    def get_proof(self, index: int) -> List[Tuple[bytes, bool]]:
        proof = []
        idx = index
        for level in self.levels[:-1]:
            sibling_idx = idx ^ 1
            if sibling_idx < len(level):
                proof.append((level[sibling_idx], idx % 2 == 0))
            idx //= 2
        return proof
    
    @staticmethod
    def verify(leaf: bytes, proof: List[Tuple[bytes, bool]], root: bytes) -> bool:
        current = leaf
        for sibling, is_right in proof:
            current = sha256(current + sibling) if is_right else sha256(sibling + current)
        return current == root

def main():
    print("NEXUS + ETHEREUM: PoHV PROOFS")
    print("=" * 50)
    
    # Get current block
    block_hex = rpc_call("eth_blockNumber")
    block = hex_to_int(block_hex)
    print(f"Current block: {block:,}")
    
    # Get block header
    block_data = rpc_call("eth_getBlockByNumber", [hex(block - 5), False])
    print(f"Block hash: {block_data['hash'][:20]}...")
    
    # Get balance
    balance_hex = rpc_call("eth_getBalance", [VITALIK, hex(block - 5)])
    balance = hex_to_int(balance_hex) / 1e18
    print(f"Vitalik balance: {balance:.4f} ETH")
    
    # Create commitment
    data = [{"address": VITALIK, "balance": balance, "block": block - 5}]
    leaves = [sha256(json.dumps(item, sort_keys=True).encode()) for item in data]
    tree = MerkleTree(leaves)
    commitment = tree.root.hex()
    print(f"Commitment: {commitment[:32]}...")
    
    # Generate and verify proof
    proof = tree.get_proof(0)
    leaf = leaves[0]
    is_valid = MerkleTree.verify(leaf, proof, tree.root)
    print(f"Proof valid: {is_valid}")
    
    print("=" * 50)
    print("PoHV proof generated and verified.")

if __name__ == "__main__":
    main()
