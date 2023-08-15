import discord
import os
import re
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


@bot.event
async def on_message(msg):
    pattern = r"(\w+://)(\w+)(.com/\w+/.+)"
    check = re.match(pattern, msg.content)
    try:
        if "twitter" not in check.group(2):
            await bot.process_commands(msg)
            return
    except AttributeError:
        await bot.process_commands(msg)
        return
    if check is not None and not msg.author.bot:
        if check.group(2) == "vxtwitter":
            await msg.channel.send(
                "I can convert it to `vxtwitter` for you. Just paste the regular `twitter` link."
            )
            await bot.process_commands(msg)
            return
        vx_twitter = re.sub(pattern, "\g<1>vxtwitter\g<3>", msg.content)
        await msg.delete()
        await msg.channel.send(f"{msg.author} sends:\n{vx_twitter}")
        await bot.process_commands(msg)
        return


@bot.command()
async def movie(ctx, *, entry):
    newline = "\n"
    link_list = []
    for title, url, popularity in generate_link(entry):
        link_list.append((f"{title}:\n{url}", popularity))
        if len(link_list) == 10:
            break
    embed = Embed(
        colour=discord.Color.dark_gold(), title=f"First 10 match for {entry}:"
    )
    link_list.sort(key=lambda x: x[1], reverse=True)
    send_list = [link[0] for link in link_list]
    embed.add_field(name="", value=f"{newline.join(send_list)}")

    await ctx.send(embed=embed)
    link_list.clear()
    send_list.clear()


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
