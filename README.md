# Nexus Protocol

A Provable, Decentralized Data Lake & Compute Fabric for Blockchains.

## What is Nexus?

Nexus provides cryptographically verifiable access to blockchain historical data. Unlike centralized RPC providers, Nexus generates **Proof of Historical Validity (PoHV)** witnesses that anyone can verify without trusting the data provider.

## Features

- **Proof of Historical Validity (PoHV)**: Merkle-based commitments linking data to Ethereum consensus
- **Ethereum Integration**: Real-time data from Alchemy with cryptographic proofs
- **On-chain Verification**: Solidity contracts for trustless proof verification
- **Proof Marketplace**: Paid verification contract for monetization

## Quick Start

```bash
# Run the Ethereum + PoHV demo
python nexus_ethereum.py

# Start the proof API
python nexus_api.py
# Then visit http://localhost:5000
```

## Files

| File | Description |
|------|-------------|
| `nexus_ethereum.py` | Fetch real Ethereum data and generate PoHV proofs |
| `nexus_api.py` | HTTP API for serving proofs |
| `eth_rpc_explorer.py` | Explore Ethereum RPC methods |
| `contracts/NexusPoHVVerifier.sol` | On-chain proof verification |
| `contracts/NexusProofMarketplace.sol` | Paid verification marketplace |

## Deploy Contracts

1. Go to [Remix](https://remix.ethereum.org)
2. Paste `contracts/NexusPoHVVerifier.sol`
3. Compile with Solidity 0.8.20+
4. Deploy to Sepolia (free) or Mainnet

## License

MIT
