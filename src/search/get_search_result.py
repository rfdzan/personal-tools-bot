import asyncio
import search.summarize_spacy as summarize_spacy
from collections import defaultdict
from os import listdir
from search._locations import Directories
from bs4 import BeautifulSoup
from aiohttp import ClientSession

APP_DIR = Directories.APP_DIR
MAIN_DIR = Directories.MAIN_DIR
SAMPLE_TEXT = Directories.SAMPLE_TEXT
BASE_URL = r"https://html.duckduckgo.com/html/?q="


async def make_request(URL: str):
    async with ClientSession() as session:
        async with session.get(URL) as resp:
            result = await resp.text()
    return result


async def parse_html(URL: str) -> list[str]:
    page_text = await make_request(URL)
    soup = BeautifulSoup(page_text, "lxml")
    body = soup.find("body", {"class": "body--html"})
    main_div = body.find("div", {"class": "serp__results"})
    inner_div = main_div.find("div", {"id": "links", "class": "results"})
    search_result = inner_div.find_all("div", {"class": True})
    found_text = []
    for result in search_result:
        text_container = result.find("a", {"class": "result__snippet"})
        if text_container is not None:
            text: str = text_container.text
            found_text.append(text.encode("utf-8"))
    return found_text


async def sanitize_result(parser, URL: str) -> set[str]:
    remove_dupe = defaultdict(int)
    results = await parser(URL)
    for result in results:
        if result not in remove_dupe.keys():
            remove_dupe[result]
    return remove_dupe


async def main(URL: str):
    sanitized = await sanitize_result(parse_html, URL=URL)
    result = [desc.decode("utf-8") for desc in sanitized]
    return " ".join(result)


def save_output(to_write: str, save: bool = True):
    if save:
        nums = [idx for idx, _ in enumerate(listdir(Directories.SAMPLE_TEXT))]
        numbering = len(nums) + 1
        with open(
            SAMPLE_TEXT.joinpath(f"text_{numbering}.txt"), "w", encoding="utf-8"
        ) as file:
            file.write(to_write)


async def search_query(entry: str):
    to_summarize = await main(BASE_URL + entry)
    result = await summarize_spacy.main(to_summarize)
    return result
