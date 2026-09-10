from outlook_client import send_outreach_graph

# Send test outreach email to yourself for verification
target_email = "kynash1@outlook.com"
company_name = "ThreeLineage Internal Test"

print(f"[*] Dispatching test outreach email to {target_email}...")
send_outreach_graph(target_email, company_name)
