use sha2::{Digest, Sha256};
use std::fs::{self, File};
use std::io::Read;
use std::path::{Path, PathBuf};
use serde::{Serialize, Deserialize};
use chrono::Utc;

const IGNORE_DIRS: &[&str] = &["target", ".git"];
const IGNORE_FILES: &[&str] = &["baseline.json", "Cargo.lock"];

#[derive(Serialize, Deserialize)]
struct Baseline {
    root: String,
    files: Vec<(String, String)>,
}

#[derive(Serialize, Deserialize)]
struct QuarantineEvent {
    timestamp: String,
    baseline_root: String,
    live_root: String,
    changed: Vec<String>,
    new: Vec<String>,
    missing: Vec<String>,
    severity: String,
    reason: String,
}

fn should_ignore(path: &Path) -> bool {
    let p = path.to_string_lossy();
    IGNORE_DIRS.iter().any(|d| p.contains(d))
        || IGNORE_FILES.iter().any(|f| p.ends_with(f))
}

fn hash_file(path: &Path) -> std::io::Result<[u8; 32]> {
    let mut file = File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buf = [0u8; 8192];
    loop {
        let n = file.read(&mut buf)?;
        if n == 0 { break; }
        hasher.update(&buf[..n]);
    }
    let result = hasher.finalize();
    let mut out = [0u8; 32];
    out.copy_from_slice(&result[..]);
    Ok(out)
}

fn collect_files(root: &Path) -> std::io::Result<Vec<PathBuf>> {
    let mut files = Vec::new();
    for entry in fs::read_dir(root)? {
        let entry = entry?;
        let path = entry.path();
        if should_ignore(&path) { continue; }
        if path.is_dir() {
            files.extend(collect_files(&path)?);
        } else if path.is_file() {
            files.push(path);
        }
    }
    Ok(files)
}

fn merkle_root(mut hashes: Vec<[u8; 32]>) -> [u8; 32] {
    while hashes.len() > 1 {
        let mut next = Vec::new();
        for chunk in hashes.chunks(2) {
            let mut hasher = Sha256::new();
            hasher.update(&chunk[0]);
            if chunk.len() == 2 { hasher.update(&chunk[1]); }
            else { hasher.update(&chunk[0]); }
            let result = hasher.finalize();
            let mut out = [0u8; 32];
            out.copy_from_slice(&result[..]);
            next.push(out);
        }
        hashes = next;
    }
    hashes[0]
}

fn to_hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{:02x}", b)).collect()
}

fn print_roots(baseline_root: &str, live_root: &str) {
    println!("=== BASELINE ROOT ===");
    println!("{}", baseline_root);
    println!("=== LIVE ROOT ===");
    println!("{}", live_root);
}

fn print_quarantine(event: &QuarantineEvent) {
    println!("=== TAMPER DETECTED ===");
    println!("timestamp: {}", event.timestamp);
    println!("severity: {}", event.severity);
    println!("reason: {}", event.reason);
    println!("baseline_root: {}", event.baseline_root);
    println!("live_root: {}", event.live_root);

    if !event.changed.is_empty() {
        println!("changed:");
        for path in &event.changed {
            println!("  {}", path);
        }
    }

    if !event.new.is_empty() {
        println!("new:");
        for path in &event.new {
            println!("  {}", path);
        }
    }

    if !event.missing.is_empty() {
        println!("missing:");
        for path in &event.missing {
            println!("  {}", path);
        }
    }
}

fn main() -> std::io::Result<()> {
    let root_path = Path::new(".");
    let baseline_path = Path::new("baseline.json");
    let quarantine_path = Path::new("quarantine.json");

    let files = collect_files(root_path)?;
    let mut hashes = Vec::new();
    let mut entries = Vec::new();

    for f in files {
        let h = hash_file(&f)?;
        let hex = to_hex(&h);
        entries.push((hex.clone(), f.display().to_string()));
        hashes.push(h);
    }

    let live_root = to_hex(&merkle_root(hashes));

    if baseline_path.exists() {
        let baseline: Baseline = serde_json::from_str(&fs::read_to_string(baseline_path)?)?;

        print_roots(&baseline.root, &live_root);

        if baseline.root != live_root {
            use std::collections::HashMap;

            let baseline_files: HashMap<String, String> =
                baseline.files.iter().cloned().collect();
            let live_files: HashMap<String, String> =
                entries.iter().cloned().collect();

            let mut changed = Vec::new();
            let mut new = Vec::new();
            let mut missing = Vec::new();

            for (_hash, path) in &entries {
                if let Some(old_hash) = baseline_files.get(path) {
                    if old_hash != _hash {
                        changed.push(path.clone());
                    }
                } else {
                    new.push(path.clone());
                }
            }

            for (_hash, path) in &baseline.files {
                if !live_files.contains_key(path) {
                    missing.push(path.clone());
                }
            }

            let event = QuarantineEvent {
                timestamp: Utc::now().to_rfc3339(),
                baseline_root: baseline.root.clone(),
                live_root: live_root.clone(),
                changed,
                new,
                missing,
                severity: "HIGH".to_string(),
                reason: "Lineage mismatch".to_string(),
            };

            fs::write(quarantine_path, serde_json::to_string_pretty(&event).unwrap())?;
            print_quarantine(&event);

            std::process::exit(1);
        } else {
            println!("[*] No tamper detected.");
            std::process::exit(0);
        }
    } else {
        let baseline = Baseline { root: live_root.clone(), files: entries };
        fs::write(baseline_path, serde_json::to_string_pretty(&baseline).unwrap())?;
        println!("[*] No baseline found — creating baseline.json");
        println!("[*] Baseline created.");
        std::process::exit(0);
    }
}
