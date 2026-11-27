#!/usr/bin/env python3
"""
Nexus Deployment Guide

Step-by-step deployment to Ethereum with cost estimates.
"""

print("""
╔═════════════════════════════════════════════════════════════════╗
║                    NEXUS DEPLOYMENT GUIDE                        ║
╚═════════════════════════════════════════════════════════════════╝

COSTS (as of now):
┌────────────────────────────────────────────────────────────────┐
│  Sepolia Testnet     FREE (test ETH from faucet)               │
│  Ethereum Mainnet    ~$5-20 to deploy contract                  │
│  Per verification    ~$1-5 in gas                               │
└────────────────────────────────────────────────────────────────┘

STEP 1: GET A WALLET
- Install MetaMask browser extension
- Create new wallet
- SAVE YOUR SEED PHRASE

STEP 2: GET TEST ETH (Sepolia - FREE)
- Go to: https://sepoliafaucet.com
- Paste your wallet address
- Get free test ETH

STEP 3: DEPLOY TO SEPOLIA (TESTNET)
1. Go to: https://remix.ethereum.org
2. Create file: NexusPoHVVerifier.sol
3. Paste the contract code
4. Compile with Solidity 0.8.20+
5. Deploy with Injected Provider - MetaMask
6. Make sure MetaMask is on Sepolia network

STEP 4: TEST THE DEPLOYMENT
- Call registerHeader with test data
- Call verifyWitnessView to test verification

STEP 5: DEPLOY TO MAINNET (COSTS REAL MONEY)
ONLY after testing on Sepolia works:
- Buy ETH on Coinbase/Kraken (~$20-50)
- Switch MetaMask to Ethereum Mainnet
- Deploy same way as Sepolia
- Cost: ~$5-20 depending on gas prices

STEP 6: START MAKING MONEY
The contract alone doesn't make money. You need:
1. CUSTOMERS who pay for proofs
2. A PAYMENT SYSTEM
3. MARKETING to reach them

WHO PAYS:
- Airdrop projects (legal liability)
- DeFi protocols (risk data)
- Auditors (compliance)
- Crypto funds (verifiable reports)

PRICING:
- Single proof: $50-200
- Monthly access: $500-2000
- Enterprise: $5000+/month

DO NOT deploy to mainnet until:
- Sepolia deployment works
- You have tested all functions
- You have at least 1 customer ready to pay
""")

# Cost calculator
print("COST CALCULATOR")
print("-" * 40)
gas_price_gwei = 20
eth_price = 3500
deploy_gas = 500000
verify_gas = 80000
deploy_cost = (deploy_gas * gas_price_gwei * 1e-9) * eth_price
verify_cost = (verify_gas * gas_price_gwei * 1e-9) * eth_price
print(f"At {gas_price_gwei} Gwei, ETH = ${eth_price}:")
print(f"  Deploy contract: ${deploy_cost:.2f}")
print(f"  Verify proof:    ${verify_cost:.2f}")
print(f"  100 verifications: ${verify_cost * 100:.2f}")
print()
print("Charge customers MORE than gas cost to profit.")
print(f"Suggested price per proof: ${max(50, verify_cost * 10):.0f}+")
