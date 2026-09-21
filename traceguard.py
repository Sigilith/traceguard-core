import os
import asyncio
import threading
import discord
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PAYMENT_LINK = os.getenv("STRIPE_PAYMENT_LINK", "https://buy.stripe.com/00wcN4df1bVb2xP7Cx3sI00")
GITHUB_REPO = os.getenv("GITHUB_REPO", "sigilith/traceguard-core")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'[+] TraceGuard bot active as {bot.user}')
    print('[*] Terminal bridge open. Type "status", "work", or "exit" below:')
    if not auto_sweep.is_running():
        auto_sweep.start()
        print('[*] Live auto-sweep engaged (running every 15 minutes).')

@bot.command(name="invite")
async def generate_invite(ctx):
    # Generates a direct authorization link for any server administrator
    client_id = bot.user.id
    invite_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot&permissions=8"
    embed = discord.Embed(
        title="🤖 TraceGuard Deployment Gateway",
        description="Click below to deploy TraceGuard into a new server and expand the bounty sweep network.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Authorization Link", value=f"[Deploy TraceGuard]({invite_url})", inline=False)
    await ctx.send(embed=embed)
    print(f"[!] Dispatched deployment link to {ctx.author} in #{ctx.channel.name}")

def scan_github_work():
    print("[*] TraceGuard scanning global GitHub for paid bounties...")
    try:
        search_url = "https://api.github.com/search/issues?q=is:open+is:issue+label:bounty&sort=created&order=desc&per_page=5"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
            
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            if items:
                print("\n[!] GLOBAL GITHUB BOUNTIES DETECTED:")
                for issue in items:
                    repo_name = issue['repository_url'].split("repos/")[-1]
                    print(f"    - {repo_name} #{issue['number']}: {issue['title']}")
                    print(f"      URL: {issue['html_url']}")
            else:
                print("[*] No new global GitHub bounties found.")
        else:
            print(f"[-] GitHub Search error (Status: {response.status_code}).")

        personal_url = f"https://api.github.com/repos/{GITHUB_REPO}/issues?state=open&per_page=3"
        pers_res = requests.get(personal_url, headers=headers)
        if pers_res.status_code == 200:
            pers_issues = [i for i in pers_res.json() if "pull_request" not in i]
            if pers_issues:
                print(f"\n[!] ACTION REQUIRED IN {GITHUB_REPO}:")
                for issue in pers_issues:
                    print(f"    - #{issue['number']}: {issue['title']} ({issue['html_url']})")

    except Exception as e:
        print(f"[-] Error connecting to GitHub: {e}")

async def scan_channels_and_github(bot):
    print("\n[*] TraceGuard running expanded bounty sweep...")
    found_any = False
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=25):
                    content_lower = message.content.lower()
                    keywords = [
                        "hire", "hiring", "paid", "bounty", "budget", 
                        "freelance", "contract", "gig", "rate", "pay", 
                        "compensation", "looking for developer", "lf dev"
                    ]
                    if any(kw in content_lower for kw in keywords) and message.author != bot.user:
                        print(f"\n[!] PAID WORK LEAD in #{channel.name} ({guild.name})!")
                        print(f"    From: {message.author}")
                        print(f"    Message: {message.content}")
                        print(f"    Link: {message.jump_url}")
                        found_any = True
            except discord.errors.Forbidden:
                continue
                
    if not found_any:
        print("[*] No Discord paid gig inquiries found in recent history.")

    scan_github_work()
    print("[*] Sweep complete.\n")

@tasks.loop(minutes=15)
async def auto_sweep():
    print("\n[LIVE] Initiating scheduled background sweep...")
    await scan_channels_and_github(bot)

def terminal_listener(bot):
    while True:
        cmd = input()
        if cmd.strip() == "work":
            asyncio.run_coroutine_threadsafe(scan_channels_and_github(bot), bot.loop)
        elif cmd.strip() == "status":
            print(f"[*] TraceGuard bot status: Online | Guilds connected: {len(bot.guilds)}")
            print(f"[*] Live auto-sweep active: {auto_sweep.is_running()}")
        elif cmd.strip() == "exit":
            print("[*] Shutting down TraceGuard bot...")
            os._exit(0)

if __name__ == "__main__":
    if not TOKEN:
        print("[-] Error: DISCORD_BOT_TOKEN not found.")
    else:
        threading.Thread(target=terminal_listener, args=(bot,), daemon=True).start()
        bot.run(TOKEN)
