import re

from discord import Message


async def check_matches_long(msg: Message):
    pattern_long = r"(\w+://www\.)(youtube)(\.com/watch\Wv=\w+)"
    matches_long = re.match(pattern_long, msg.content, re.IGNORECASE)
    if matches_long is None:
        return matches_long
    if matches_long.group(2) != "youtube":
        return None
    converted_link = re.sub(pattern_long, "\g<1>ymusicapp\g<3>", msg.content)
    return converted_link


async def check_matches_short(msg: Message):
    pattern_short = r"(\w+://)(youtu.be/)(\w+)"
    matches_short = re.match(pattern_short, msg.content, re.IGNORECASE)
    if matches_short is None:
        return matches_short
    if matches_short.group(2) != "youtu.be/":
        return None
    converted_link = re.sub(
        pattern_short, "\g<1>ymusicapp.com/watch?v=\g<3>", msg.content
    )
    return converted_link


async def ymusicapp(msg: Message):
    result_long = await check_matches_long(msg)
    result_short = await check_matches_short(msg)
    if all((result_short is None, result_long is None)):
        return msg
    converted_link = result_long if result_long is not None else result_short
    await msg.channel.send(converted_link)
    return msg
