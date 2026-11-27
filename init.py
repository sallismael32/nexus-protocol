#!/usr/bin/env python3
"""
Nexus Project Initializer

Sets up the Nexus project structure and configuration.
Run: python init.py
"""

import os
from pathlib import Path

def init():
    print("=" * 50)
    print("  NEXUS PROJECT INITIALIZER")
    print("=" * 50)
    
    dirs = ["contracts", "python", "proofs", "data"]
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
        print(f"  [OK] Created {d}/")
    
    env_file = Path(".env")
    if not env_file.exists():
        env_file.write_text("ALCHEMY_API_KEY=your_api_key_here\n")
        print("  [OK] Created .env template")
    else:
        print("  [SKIP] .env already exists")
    
    gitignore = Path(".gitignore")
    if not gitignore.exists():
        gitignore.write_text(".env\n__pycache__/\n*.pyc\nproofs/\ndata/\n.venv/\nvenv/\n")
        print("  [OK] Created .gitignore")
    
    api_key = os.environ.get("ALCHEMY_API_KEY", "")
    if api_key and api_key != "your_api_key_here":
        print(f"  [OK] API key found: {api_key[:10]}...")
    else:
        print("  [WARN] Set ALCHEMY_API_KEY in .env or environment")
    
    print()
    print("=" * 50)
    print("  INITIALIZATION COMPLETE")
    print("=" * 50)
    print()
    print("Next steps:")
    print("  1. Add your Alchemy API key to .env")
    print("  2. Run: python python/nexus_ethereum.py")
    print("  3. Deploy contracts from contracts/")
    print()

if __name__ == "__main__":
    init()
