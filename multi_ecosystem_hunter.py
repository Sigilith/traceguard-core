import subprocess
import json
import os

print("[*] [Multi-Ecosystem Hunter] Expanding hunt parameters across Web3, AI governance, and enterprise infrastructure...")

# Define high-value ecosystem targets
ecosystems = [
    {"name": "AI & LLM Orchestration", "target_repo": "vllm-project/vllm", "tier": "high"},
    {"name": "Autonomous Agent Tooling", "target_repo": "knowall-ai/zaplie-bot", "tier": "high"},
    {"name": "Rustchain Consensus & Nodes", "target_repo": "Scottcjn/rustchain-bounties", "tier": "critical"},
    {"name": "Decentralized Governance", "target_repo": "nebgov/nebgov", "tier": "high"}
]

print(f"[+] Loaded {len(ecosystems)} high-priority target ecosystems.")
for eco in ecosystems:
    print(f"  - Targeting [{eco['tier'].upper()}] {eco['name']} ({eco['target_repo']})")

print("\n[*] Initializing multi-ecosystem probe sequence...")
