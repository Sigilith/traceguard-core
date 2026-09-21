import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

PAYMENT_LINK = "https://buy.stripe.com/your_actual_link_here"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'[+] Payment Sentry active as {bot.user}')

@bot.command(name="pay")
async def send_payment_link(ctx):
    author = ctx.author
    embed = discord.Embed(
        title="🔒 Secure Checkout",
        description="Click below to complete your transaction safely.",
        color=discord.Color.green()
    )
    embed.add_field(name="Payment Portal", value=f"[Access Checkout Window]({PAYMENT_LINK})", inline=False)
    
    try:
        await author.send(embed=embed)
        await ctx.message.add_reaction("✅")
        print(f"[!] Dispatched payment link privately to {author}")
    except discord.errors.Forbidden:
        await ctx.send(f"{author.mention}, here is your secure checkout link: {PAYMENT_LINK}", embed=embed)
        print(f"[!] Dispatched payment link publicly to channel for {author}")

if __name__ == "__main__":
    if not TOKEN:
        print("[-] Error: DISCORD_BOT_TOKEN not found in environment variables or .env file.")
    else:
        bot.run(TOKEN)
