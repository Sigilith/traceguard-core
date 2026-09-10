use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::process;
use std::collections::hash_map::DefaultHasher;
use std::hash::Hasher;

fn hash_file(path: &Path) -> u64 {
    if let Ok(content) = fs::read(path) {
        let mut hasher = DefaultHasher::new();
        hasher.write(&content);
        hasher.finish()
    } else {
        0
    }
}

fn load_baseline() -> HashMap<String, u64> {
    if let Ok(data) = fs::read_to_string("baseline.json") {
        let mut map = HashMap::new();
        for line in data.lines() {
            let parts: Vec<&str> = line.split('|').collect();
            if parts.len() == 2 {
                if let Ok(h) = parts[1].parse::<u64>() {
                    map.insert(parts[0].to_string(), h);
                }
            }
        }
        map
    } else {
        HashMap::new()
    }
}

fn save_baseline(map: &HashMap<String, u64>) {
    let mut content = String::new();
    for (k, v) in map {
        content.push_str(&format!("{}|{}\n", k, v));
    }
    let _ = fs::write("baseline.json", content);
}

fn main() {
    let mut current_files = HashMap::new();
    if let Ok(entries) = fs::read_dir(".") {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_file() {
                if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                    if name == "baseline.json" || name == "quarantine.json" || name.starts_with('.') {
                        continue;
                    }
                    current_files.insert(name.to_string(), hash_file(&path));
                }
            }
        }
    }

    if !Path::new("baseline.json").exists() {
        save_baseline(&current_files);
        println!("NO TAMPER");
        process::exit(0);
    }

    let baseline = load_baseline();

    let mut changed = vec![];
    let mut missing = vec![];
    let mut new_files = vec![];

    for (k, &v) in &current_files {
        match baseline.get(k) {
            Some(&bv) if bv != v => changed.push(k.clone()),
            None => new_files.push(k.clone()),
            _ => {}
        }
    }

    for k in baseline.keys() {
        if !current_files.contains_key(k) {
            missing.push(k.clone());
        }
    }

    if !changed.is_empty() || !missing.is_empty() || !new_files.is_empty() {
        println!("TAMPER DETECTED");
        println!("Changed: {:?}", changed);
        println!("Missing: {:?}", missing);
        println!("New: {:?}", new_files);

        let quarantine_report = format!(
            "{{\n  \"status\": \"TAMPER_DETECTED\",\n  \"changed\": {:?},\n  \"missing\": {:?},\n  \"new\": {:?}\n}}",
            changed, missing, new_files
        );
        let _ = fs::write("quarantine.json", quarantine_report);
        process::exit(1);
    }

    println!("NO TAMPER");
    process::exit(0);
}
