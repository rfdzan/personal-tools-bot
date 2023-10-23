import re

from discord import Message


async def vxtwitter(msg: Message) -> None | Message:
    thanks_for_nothing_elon = ("x", "twitter")
    pattern = r"(\w+://)(\w+)(.com/\w+/.+)"
    check = re.match(pattern, msg.content, re.IGNORECASE)
    if check is None:
        return check
    if check.group(2) not in thanks_for_nothing_elon:
        return None
    if check.group(2) == "vxtwitter":
        await msg.channel.send(
            "I can convert it to `vxtwitter` for you. "
            "Just paste the regular `twitter` link."
        )
        return None
    vx_twitter = re.sub(pattern, "\g<1>vxtwitter\g<3>", msg.content)
    await msg.delete()
    await msg.channel.send(f"{msg.author} sends:\n{vx_twitter}")
    return msg
