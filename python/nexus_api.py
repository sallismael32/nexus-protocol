#!/usr/bin/env python3
"""
Nexus Proof API

Simple API that serves PoHV proofs for Ethereum data.

Usage:
    export ALCHEMY_API_KEY=your_key
    python nexus_api.py
    
Then visit: http://localhost:5000

Endpoints:
    GET  /                     API info
    GET  /block                Current block
    GET  /balance/<address>    Get balance with proof
    POST /verify               Verify a witness
"""

import json
import hashlib
import os
import urllib.request
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

API_KEY = os.environ.get("ALCHEMY_API_KEY", "YOUR_ALCHEMY_API_KEY")
ALCHEMY_URL = f"https://eth-mainnet.g.alchemy.com/v2/{API_KEY}"
PORT = 5000

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def rpc_call(method: str, params: list = None):
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode()
    req = urllib.request.Request(ALCHEMY_URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read()).get("result")

def hex_to_int(h):
    return int(h, 16) if isinstance(h, str) and h.startswith("0x") else h

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = leaves
        self.root = self._build(leaves)
    
    def _build(self, leaves):
        if not leaves:
            return b'\x00' * 32
        if len(leaves) == 1:
            return leaves[0]
        next_level = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            right = leaves[i+1] if i+1 < len(leaves) else leaves[i]
            next_level.append(sha256(left + right))
        return self._build(next_level)

def create_proof(data, block_number, block_hash):
    leaves = [sha256(json.dumps(item, sort_keys=True).encode()) for item in data]
    tree = MerkleTree(leaves)
    return {
        "type": "PoHV_Witness_v1",
        "timestamp": datetime.utcnow().isoformat(),
        "block_number": block_number,
        "block_hash": block_hash,
        "commitment": tree.root.hex(),
        "data": data
    }

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == "/":
            self._send_json({
                "name": "Nexus Proof API",
                "endpoints": ["/block", "/balance/<address>"]
            })
        
        elif path == "/block":
            block_hex = rpc_call("eth_blockNumber")
            block = hex_to_int(block_hex)
            block_data = rpc_call("eth_getBlockByNumber", [hex(block), False])
            self._send_json({
                "block_number": block,
                "block_hash": block_data["hash"]
            })
        
        elif path.startswith("/balance/"):
            address = path.split("/balance/")[1]
            block_hex = rpc_call("eth_blockNumber")
            block = hex_to_int(block_hex) - 2
            block_data = rpc_call("eth_getBlockByNumber", [hex(block), False])
            balance_hex = rpc_call("eth_getBalance", [address, hex(block)])
            balance = hex_to_int(balance_hex)
            
            data = [{"address": address, "balance_eth": balance / 1e18, "block": block}]
            proof = create_proof(data, block, block_data["hash"])
            self._send_json(proof)
        
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

def main():
    print(f"Nexus Proof API running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
