from discord import Message

from .twitter_replace import vxtwitter
from .ytvid_replace import ymusicapp


async def main(msg: Message, replace_yt: bool):
    to_replace = {
        True: (await vxtwitter(msg), await ymusicapp(msg)),
        False: (await vxtwitter(msg),),
    }
    msg_list = to_replace.get(replace_yt)
    print(msg_list)
    check = [msg is None for msg in msg_list]
    print(check)
    if all(check):
        return None
    for msg in msg_list:
        if msg is not None:
            return msg
