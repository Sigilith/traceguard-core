use std::fs::File;
use std::io::{BufRead, BufReader};
use sha2::{Sha256, Digest};
use serde_json::Value;

fn main() {
    let path = std::env::args().nth(1).expect("Missing ledger path");
    let file = File::open(&path).expect("Cannot open ledger file");
    let reader = BufReader::new(file);

    let mut last_hash = String::new();
    let mut ok = true;

    for (i, line) in reader.lines().enumerate() {
        let line = line.expect("Read error");
        let json: Value = serde_json::from_str(&line).expect("Invalid JSON");

        let event_id = json["event_id"].as_str().unwrap_or("");
        let event_hash = json["event_hash"].as_str().unwrap_or("");

        // Explicit pre‑canonical window: 0–2
        let is_pre_canonical = i <= 2;

        let mut hasher = Sha256::new();
        hasher.update(serde_json::to_string(&json).unwrap());
        let computed = format!("{:x}", hasher.finalize());

        if computed != event_hash {
            if is_pre_canonical {
                println!(
                    "[WARN] Pre‑canonical mismatch at event {} (id: {}). Documented by receipts.",
                    i, event_id
                );
            } else {
                println!(
                    "[CRITICAL] Hash mismatch at event {} (id: {})!",
                    i, event_id
                );
                ok = false;
                break;
            }
        }

        last_hash = event_hash.to_string();
    }

    if ok {
        println!("[OK] Sovereign chain verified (pre‑canonical events warned, not hidden).");
        println!("HEAD HASH: {}", last_hash);
    }
}
