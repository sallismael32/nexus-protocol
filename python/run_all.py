#!/usr/bin/env python3
"""
Nexus + Alchemy — Run Everything (Windows-compatible)

Usage:
    python run_all.py
"""

import os
import sys
import json
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

def load_api_key():
    key = os.environ.get("ALCHEMY_API_KEY", "")
    if key:
        return key
    for env_path in [SCRIPT_DIR / ".env", SCRIPT_DIR / "ismails-first-app" / ".env"]:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("ALCHEMY_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("'\"")
    return "YOUR_ALCHEMY_API_KEY"

API_KEY = load_api_key()

def header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_alchemy():
    header("ALCHEMY CONNECTION")
    if not API_KEY or API_KEY == "YOUR_ALCHEMY_API_KEY":
        print("  [FAIL] Set ALCHEMY_API_KEY environment variable")
        return False
    print(f"  API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    url = f"https://eth-mainnet.g.alchemy.com/v2/{API_KEY}"
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []}).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if "result" in result:
                block = int(result["result"], 16)
                print(f"  Connected to Ethereum mainnet")
                print(f"  Current block: {block:,}")
                print("  [OK]")
                return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False

def main():
    print("\n" + "#" * 60)
    print("#" + " " * 18 + "NEXUS + ALCHEMY" + " " * 19 + "#")
    print("#" * 60)
    test_alchemy()
    print("\n" + "#" * 60)

if __name__ == "__main__":
    main()
