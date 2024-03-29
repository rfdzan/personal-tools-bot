import os
import re

import discord
from discord import Embed, Message
from discord.ext import commands
from dotenv import load_dotenv

from bot.master_tools import master_query
from bot.tmdb_search import generate_link
from bot.tokopedia_search import main
from msg_replace.replace_main import main as replace_main
from search.get_search_result import search_query
from steam_search.search_game import handle_result as steam_result

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("testbot is running")
    await bot.change_presence(activity=discord.Game(name="!movie"))


@bot.event
async def on_message(msg: Message):
    if msg.author.bot:
        return
    await replace_main(msg, replace_yt=True)
    await bot.process_commands(msg)


@bot.command()
async def movie(ctx, *, entry):
    newline = "\n"
    link_list = []
    _type = "movie"
    for title, url, popularity in generate_link(entry, _type):
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
async def tv(ctx, *, entry):
    newline = "\n"
    link_list = []
    _type = "tv"
    for title, url, popularity in generate_link(entry, _type):
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
async def search(ctx, *entry):
    footer_display = " ".join(entry)
    search_term = "+".join(entry)
    result = await search_query(search_term)
    embed = Embed(colour=discord.Color.dark_gold())
    embed.add_field(name="", value=f"```{result}```")
    embed.set_footer(text=f"Result for: {footer_display}")
    await ctx.send(embed=embed)


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


@bot.command()
async def shop(ctx, *entry):
    search = " ".join(entry)
    results = await main(search)
    embed = Embed(colour=discord.Color.dark_gold())
    display = []
    for idx, result in enumerate(results):
        if idx == 7:
            break
        link = f"[{result.get('name')}]({result.get('product_url')})"
        _sold = [str(result.get("sold")[0]), result.get("sold")[1]]
        title = (
            f"{result.get('price')}, {''.join(_sold)}, {result.get('product_rating')}"
        )
        display.append(f"{title}\n{link}")
    print(len(display))
    embed.add_field(name="", value="\n".join(display[0:3]))
    embed.add_field(name="", value="\n".join(display[3:6]))
    await ctx.send(embed=embed)
    display.clear()

@bot.command()
async def steam(ctx, *entry):
    newline = "\n"
    search_term = " ".join(entry)
    result = await steam_result(search_term)
    if result is None:
        return None
    info = result[0]
    send_info = [info[0], info[1], info[3]]
    link = info[2]
    price = result[1]
    if isinstance(price, list):
        price = newline.join([f"{price[1]} {price[0]}", price[2]])
    embed = Embed(colour=discord.Color.dark_gold())
    embed.add_field(name="", value=f"{newline.join(send_info)}{newline}{newline}{price}")
    await ctx.send(embed=embed)
    await ctx.send(re.sub(r"/\?snr=.+", "", link))

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if token is None:
        raise ValueError("Token not found.")
    bot.run(token)
