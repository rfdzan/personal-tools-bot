from discord import Message

from .twitter_replace import vxtwitter
from .ytvid_replace import ymusicapp


async def main(msg: Message, replace_yt: bool) -> None:
    to_replace = {
        True: (vxtwitter, ymusicapp),
        False: (vxtwitter,),
    }
    replace_func_list = to_replace.get(replace_yt)
    if replace_func_list is None:
        return None
    check = [await func(msg) is None for func in replace_func_list]
    if all(check):
        return None
    return None
