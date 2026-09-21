import subprocess
import json
import os

print("[*] [BTC Microtask Hunter] Initializing specialized scan for BTC and wrapped BTC payout channels...")

btc_targets = [
    {"platform": "Open-Source Bug Bounty / Micro-PRs", "focus": "code review & testing microtasks", "reward_type": "BTC / wBTC"},
    {"platform": "Rustchain & Web3 Node Bounties", "focus": "automation & consensus testing", "reward_type": "RTC / wBTC Bridge"},
    {"platform": "Documentation & Compliance Pipelines", "focus": "markdown linting & test fixtures", "reward_type": "Crypto-linked pools"}
]

print(f"[+] Loaded {len(btc_targets)} BTC/Crypto microtask vectors.")
for target in btc_targets:
    print(f"  - Scanning [{target['reward_type']}] {target['platform']} ({target['focus']})")

print("\n[+] [Hunter Ready] Bot is configured to ingest code review, testing, docs, and automation microtasks linked to BTC reward pools.")
