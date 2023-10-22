import re


async def vxtwitter(bot, msg):
    thanks_for_nothing_elon = ("x", "twitter")
    pattern = r"(\w+://)(\w+)(.com/\w+/.+)"
    check = re.match(pattern, msg.content)
    try:
        if check.group(2) not in thanks_for_nothing_elon:
            await bot.process_commands(msg)
            return
    except AttributeError:
        await bot.process_commands(msg)
        return
    if check is not None and not msg.author.bot:
        if check.group(2) == "vxtwitter":
            await msg.channel.send(
                "I can convert it to `vxtwitter` for you. "
                "Just paste the regular `twitter` link."
            )
            await bot.process_commands(msg)
            return
        vx_twitter = re.sub(pattern, "\g<1>vxtwitter\g<3>", msg.content)
        await msg.delete()
        await msg.channel.send(f"{msg.author} sends:\n{vx_twitter}")
        await bot.process_commands(msg)
        return
