#!/usr/bin/env python3
"""
Ethereum RPC Methods Explorer

Explores common Ethereum JSON-RPC methods via Alchemy.
Run: python eth_rpc_explorer.py

Set ALCHEMY_API_KEY environment variable before running.
"""

import json
import os
import urllib.request
from datetime import datetime

API_KEY = os.environ.get("ALCHEMY_API_KEY", "YOUR_ALCHEMY_API_KEY")
BASE_URL = f"https://eth-mainnet.g.alchemy.com/v2/{API_KEY}"

VITALIK = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

def rpc_call(method, params=None):
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode()
    req = urllib.request.Request(BASE_URL, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            return result.get("result") if "error" not in result else {"error": result["error"]}
    except Exception as e:
        return {"error": str(e)}

def hex_to_int(h):
    return int(h, 16) if isinstance(h, str) and h.startswith("0x") else h

def main():
    print("ETHEREUM RPC METHODS EXPLORER")
    print("=" * 40)
    
    # Block number
    block_hex = rpc_call("eth_blockNumber")
    if isinstance(block_hex, str):
        print(f"Current block: {hex_to_int(block_hex):,}")
    
    # Balance
    balance_hex = rpc_call("eth_getBalance", [VITALIK, "latest"])
    if isinstance(balance_hex, str):
        print(f"Vitalik balance: {hex_to_int(balance_hex) / 1e18:.4f} ETH")
    
    # Gas price
    gas_hex = rpc_call("eth_gasPrice")
    if isinstance(gas_hex, str):
        print(f"Gas price: {hex_to_int(gas_hex) / 1e9:.2f} Gwei")
    
    print("=" * 40)
    print("Done.")

if __name__ == "__main__":
    main()
