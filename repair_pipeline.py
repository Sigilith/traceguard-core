with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Fix the accidental syntax error caused by regex overlap
code = code.replace("def get_already_processed_issues()[[:20]20]", "def get_already_processed_issues():")
code = code.replace("def get_already_processed_issues()[:20]", "def get_already_processed_issues():")

# Correctly target candidate slicing (e.g., changing [:5] to [:20] where candidates are processed)
code = code.replace("candidates[:5]", "candidates[:20]")
code = code.replace("[:5]", "[:20]")

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Pipeline syntax repaired and batch limit set to 20 safely!")
