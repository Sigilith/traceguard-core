#!/bin/bash
# Step 1: Subdomain Enumeration
subfinder -d santos.com -silent -o subdomains.txt

# Step 2: Live HTTP Service Probing
httpx -l subdomains.txt -silent -mc 200,301,302,403 -o live_targets.txt

# Step 3: Endpoint Directory Discovery on the main domain
ffuf -u https://santos.com/FUZZ -w common.txt -mc 200 -s -o ffuf_results.json
