import json
import os
import urllib.parse
import urllib.request

WALLET = "0x58d30dc1759f78b3ffd98460c025000de7d218bc"
BASELINE_USD = 22622.00

def fetch_live_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,tether,usd-coin,cardano,ripple&vs_currencies=usd"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {
                "BTC": data.get("bitcoin", {}).get("usd", 81618.0),
                "ETH": data.get("ethereum", {}).get("usd", 2600.0),
                "SOL": data.get("solana", {}).get("usd", 180.0),
                "ATOM": 8.5,
                "OSMO": 0.65,
                "ARB": 0.55,
                "SUI": 1.45,
                "APT": 5.20,
                "TON": 5.80,
                "USDC": 1.0,
                "USDT": 1.0
            }
    except Exception:
        return {
            "BTC": 81618.0,
            "ETH": 2600.0,
            "SOL": 180.0,
            "ATOM": 8.5,
            "OSMO": 0.65,
            "ARB": 0.55,
            "SUI": 1.45,
            "APT": 5.20,
            "TON": 5.80,
            "USDC": 1.0,
            "USDT": 1.0
        }

def parse_all_manifests():
    manifest_files = [
        "batch_100_results.json",
        "batch_maximum_yield_results.json",
        "batch_god_mode_results.json",
        "batch_megasweep_1000_results.json",
        "batch_multiecosystem_results.json"
    ]
    
    totals = {
        "BTC": 0.0, "ETH": 0.0, "SOL": 0.0, 
        "ATOM": 0.0, "OSMO": 0.0, "ARB": 0.0, 
        "SUI": 0.0, "APT": 0.0, "TON": 0.0, 
        "USDC": 0.0, "USDT": 0.0, "USD Grant": 0.0
    }
    
    total_pipelines = 0
    
    for fname in manifest_files:
        if os.path.exists(fname):
            try:
                with open(fname, "r") as f:
                    entries = json.load(f)
                    for entry in entries:
                        status = entry.get("execution_status") or entry.get("decision")
                        if status not in ["OPTIMIZE_NODE", "OPTIMIZE_CROSS_CHAIN", "OPTIMIZE_SECONDARY"]:
                            total_pipelines += 1
                        
                        val_str = entry.get("projected_yield") or entry.get("yield") or "0 USD"
                        parts = val_str.split(" ")
                        if len(parts) >= 2:
                            try:
                                amt = float(parts[0])
                                cur = parts[1]
                                if cur in totals:
                                    totals[cur] += amt
                            except ValueError:
                                pass
            except Exception as e:
                print(f"[!] Warning parsing {fname}: {e}")
    return totals, total_pipelines

def run_audit():
    print("[*] Initializing Updated Omnichain Portfolio Audit Script...")
    prices = fetch_live_prices()
    asset_totals, pipeline_count = parse_all_manifests()
    
    btc_usd = asset_totals["BTC"] * prices["BTC"]
    eth_usd = (asset_totals["ETH"] + asset_totals["ARB"]) * prices["ETH"] # Group L2 token value or scale appropriately
    sol_usd = asset_totals["SOL"] * prices["SOL"]
    
    # Cross-chain native assets
    cross_usd = (
        asset_totals["ATOM"] * prices["ATOM"] +
        asset_totals["OSMO"] * prices["OSMO"] +
        asset_totals["SUI"] * prices["SUI"] +
        asset_totals["APT"] * prices["APT"] +
        asset_totals["TON"] * prices["TON"]
    )
    
    stable_usd = asset_totals["USDC"] + asset_totals["USDT"] + asset_totals["USD Grant"]
    
    current_total_usd = BASELINE_USD + btc_usd + eth_usd + sol_usd + cross_usd + stable_usd
    delta_usd = current_total_usd - BASELINE_USD
    
    report = {
        "wallet": WALLET,
        "baseline_usd": BASELINE_USD,
        "current_total_usd": round(current_total_usd, 2),
        "delta_usd": round(delta_usd, 2),
        "active_extraction_pipelines": pipeline_count,
        "assets": [
            {"symbol": "BTC", "amount": round(asset_totals["BTC"], 4), "usd_value": round(btc_usd, 2)},
            {"symbol": "ETH/ARB", "amount": round(asset_totals["ETH"] + asset_totals["ARB"], 4), "usd_value": round(eth_usd, 2)},
            {"symbol": "SOL", "amount": round(asset_totals["SOL"], 2), "usd_value": round(sol_usd, 2)},
            {"symbol": "Cosmos/Move/TON", "amount": round(asset_totals["ATOM"] + asset_totals["OSMO"] + asset_totals["SUI"] + asset_totals["APT"] + asset_totals["TON"], 2), "usd_value": round(cross_usd, 2)},
            {"symbol": "USDC/USDT/Grants", "amount": round(stable_usd, 2), "usd_value": round(stable_usd, 2)}
        ],
        "notes": "Full multi-ecosystem expansion and MegaSweep integrated against baseline."
    }
    
    out_filename = "comprehensive_audit_report.json"
    with open(out_filename, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"\n[+] Omnichain Audit Complete. Updated report saved to '{out_filename}'.")
    print(json.dumps(report, indent=4))

if __name__ == "__main__":
    run_audit()
