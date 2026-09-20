import os
import discord
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

SECRET_PATTERNS = {
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "GitHub Classic Token": r"ghp_[a-zA-Z0-9]{36}",
    "Discord Bot Token": r"[MNO][a-zA-Z0-9_-]{23,25}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}"
}

class TraceGuardDLP(discord.Client):
    async def on_ready(self):
        print(f'[+] DLP Containment Boundary active as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        for secret_type, pattern in SECRET_PATTERNS.items():
            if re.search(pattern, message.content):
                try:
                    await message.delete()
                except discord.errors.Forbidden:
                    print(f"[-] Error: Bot lacks 'Manage Messages' permission.")
                    return
                
                warning = f"⚠️ **Security Alert:** Your message in `{message.channel.name}` was blocked because it contained a `{secret_type}`. Please rotate this credential immediately."
                await message.author.send(warning)
                print(f"[!] BLOCKED: {secret_type} leak attempted by {message.author}")
                return

intents = discord.Intents.default()
intents.message_content = True

if __name__ == "__main__":
    client = TraceGuardDLP(intents=intents)
    client.run(TOKEN)
