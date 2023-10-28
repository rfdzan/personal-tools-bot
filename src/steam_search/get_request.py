import asyncio
import json
import re

import aiofiles
import httpx

from .constants import FILES


async def url_edit(url: str, search: str) -> str:
    pattern = r"(\?term=)(<\w+>)"
    search_term = re.sub(pattern, f"\g<1>{search.replace(' ', '+')}", url)
    return search_term


async def generate_link(search: str) -> str:
    async with aiofiles.open(FILES.joinpath("url.json")) as f:
        url_dict = json.loads(await f.read())
    url = url_dict.get("url")
    product_url = await url_edit(url, search)
    return product_url


async def make_request(url: str) -> str:
    async with httpx.AsyncClient() as aclient:
        result = await aclient.get(url)
    return result.text


async def main(search: str):
    search_url = await generate_link(search)
    response = await make_request(search_url)
    return response


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        r = runner.run(main("Titanfall"))
    print(r)
