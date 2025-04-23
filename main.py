import os
from loguru import logger
from dupr_client import DuprClient
from dotenv import load_dotenv
from typing import Final
import discord
from discord.ext import commands
import re

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

dupr = DuprClient()

def dupr_auth():
    username = os.getenv("DUPR_USERNAME")
    password = os.getenv("DUPR_PASSWORD")
    dupr.auth_user(username, password)

def update_nickname(pid) -> str:
    _, player_data = dupr.get_player(pid)
    name = player_data["fullName"]
    rating_single = player_data["ratings"]["singles"]
    rating_double = player_data["ratings"]["doubles"]

    # Parse the ratings
    single_value = parse_rating(rating_single)
    double_value = parse_rating(rating_double)

    valid_ratings = [r for r in [single_value, double_value] if r is not None]
    highest_rating = max(valid_ratings) if valid_ratings else "NR"

    return f"{name} ({highest_rating})"

def parse_rating(rating_str):
    return float(rating_str) if rating_str != "NR" else None

#--------# BOT COMMANDS #--------#

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.command(name='verify')
async def verify(ctx, *, raw_input):
    
    # Clean up user's message
    await ctx.message.delete()

    # Try to extract PID from any part of the input
    pid_match = re.search(r"\b\d{7,}\b", raw_input)
    if not pid_match:
        await ctx.send("❌ Couldn't find a valid DUPR ID in your message.")
        return

    pid = pid_match.group(0)
    
    # Attempt to update nickname
    nickname = update_nickname(pid)
    try:
        await ctx.author.edit(nick=nickname)
        await ctx.send(f"✅ Your nickname has been set to `{nickname}`.")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to change your nickname.")
        return
    except Exception as e:
        await ctx.send(f"⚠️ Something went wrong: {e}")
        return

    # Add role
    role_name = "DUPR Verified"
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        try:
            await ctx.author.add_roles(role)
            await ctx.send(f"✅ You've been added to the **{role_name}** role.")
        except discord.Forbidden:
            await ctx.send(f"❌ I don't have permission to add you to the `{role_name}` role.")
            return
        except Exception as e:
            await ctx.send(f"⚠️ Something went wrong while assigning the role: {e}")
            return
    else:
        await ctx.send(f"⚠️ Role `{role_name}` not found. Please ask an admin to create it.")

bot.run(TOKEN)