use sha2::{Sha256, Digest};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;
use serde_json::Value;

fn main() {
    let possible_paths = [".lineage/collisions.jsonl", "../.lineage/collisions.jsonl"];
    let mut ledger_path = None;

    for path in &possible_paths {
        if Path::new(path).exists() {
            ledger_path = Some(*path);
            break;
        }
    }

    let path = match ledger_path {
        Some(p) => p,
        None => {
            println!("[+] Ledger path not found or empty. Genesis state clean.");
            std::process::exit(0);
        }
    };

    println!("[*] Verifying integrity of ledger at: {}", path);
    let file = match File::open(path) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("[CRITICAL] Failed to open collision ledger at {}: {}", path, e);
            std::process::exit(1);
        }
    };

    let reader = BufReader::new(file);
    let mut expected_prev_hash = "genesis_root_00000000000000000000000000000000".to_string();
    let mut line_num = 0;
    let mut record_count = 0;

    for line in reader.lines() {
        line_num += 1;
        let line_content = match line {
            Ok(l) => l,
            Err(e) => {
                eprintln!("[CRITICAL] Ledger read error at line {}: {}", line_num, e);
                std::process::exit(1);
            }
        };

        if line_content.trim().is_empty() {
            continue;
        }

        let mut parsed: Value = match serde_json::from_str(&line_content) {
            Ok(v) => v,
            Err(e) => {
                eprintln!("[CRITICAL] Invalid JSON structure at line {}: {}", line_num, e);
                std::process::exit(1);
            }
        };

        let recorded_prev = parsed["previous_evidence_hash"].as_str().unwrap_or("");
        if recorded_prev != expected_prev_hash {
            eprintln!("[CRITICAL] Hash chain fracture detected at line {}!", line_num);
            eprintln!("    Expected Prev: {}", expected_prev_hash);
            eprintln!("    Recorded Prev: {}", recorded_prev);
            std::process::exit(1);
        }

        let recorded_hash = parsed["evidence_hash"].as_str().unwrap_or("").to_string();
        
        // Remove evidence_hash to reconstruct the exact canonical payload state before hashing
        if let Some(obj) = parsed.as_object_mut() {
            obj.remove("evidence_hash");
        }

        let canonical_data = serde_json::to_string(&parsed).unwrap();
        let mut hasher = Sha256::new();
        hasher.update((expected_prev_hash.clone() + &canonical_data).as_bytes());
        let computed_hash = hex::encode(hasher.finalize());

        if computed_hash != recorded_hash {
            eprintln!("[CRITICAL] Cryptographic signature mismatch at line {}!", line_num);
            eprintln!("    Computed: {}", computed_hash);
            eprintln!("    Recorded: {}", recorded_hash);
            std::process::exit(1);
        }

        expected_prev_hash = recorded_hash;
        record_count += 1;
    }

    println!("[+] Ledger Integrity Verified: {} sequential records validated successfully.", record_count);
    std::process::exit(0);
}
