with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Clean up any trailing malformed commas or bracket issues in the ledger/json write block
code = code.replace(',\n    }', '\n    }')

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Final dictionary syntax cleaned!")
