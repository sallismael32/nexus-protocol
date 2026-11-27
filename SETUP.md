# Setup Instructions

## 1. Get an Alchemy API Key

1. Go to [alchemy.com](https://alchemy.com)
2. Create a free account
3. Create an app for Ethereum Mainnet
4. Copy your API key

## 2. Set the API Key

```bash
# Option A: Environment variable
export ALCHEMY_API_KEY=your_key_here

# Option B: Create .env file
echo "ALCHEMY_API_KEY=your_key_here" > .env
```

## 3. Run the Scripts

```bash
# Test Ethereum connection
python python/run_all.py

# Full PoHV demo (download from Releases or clone and add your key)
python nexus_ethereum.py
```

## 4. Deploy Contracts

1. Go to [Remix](https://remix.ethereum.org)
2. Create new file, paste `contracts/NexusPoHVVerifier.sol`
3. Compile with Solidity 0.8.20+
4. Deploy to Sepolia testnet (free) or Mainnet

## Files Structure

```
nexus-protocol/
├── contracts/
│   ├── NexusPoHVVerifier.sol      # On-chain proof verification
│   └── NexusProofMarketplace.sol   # Paid verification
├── python/
│   └── run_all.py                  # Quick test script
├── README.md
├── SETUP.md
├── requirements.txt
└── .gitignore
```

## Next Steps

1. Deploy to Sepolia testnet
2. Test all functions
3. Find customers who need verifiable data
4. Deploy to mainnet when ready
