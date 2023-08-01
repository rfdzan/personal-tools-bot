import discord
import os
from bot.search import generate_link
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("bot is running")
    await bot.change_presence(activity=discord.Game(name="!movie"))


@bot.command()
async def movie(ctx, *, entry):
    newline = "\n"
    link_list = []
    for title, url in generate_link(entry):
        link_list.append(f"{title}:\n{url}")
        if len(link_list) == 10:
            break
    embed = Embed(
        colour=discord.Color.dark_gold(), title=f"First 10 match for {entry}:"
    )
    link_list.sort()
    embed.add_field(name="", value=f"{newline.join(link_list)}")

    await ctx.send(embed=embed)
    link_list.clear()


load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))
