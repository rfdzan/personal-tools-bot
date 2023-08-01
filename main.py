import discord
import os
from bot.search import generate_link
from bot.master_tools import master_query
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="test!", intents=intents, help_command=None)


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


@bot.command()
@commands.is_owner()
async def query(ctx, *, query):
    count = 0
    query_result = master_query(query)
    if isinstance(query_result, str):
        await ctx.send("banned command.")
    else:
        for data in query_result:
            count += 1
            if count == 5:
                count = 0
                break
            await ctx.send(data)


load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))
