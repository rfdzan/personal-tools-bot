import asyncio

from .parse_html import main


async def search(search_term: str) -> dict[str, int | str | dict[str, str]] | None:
    result = await main(search_term)
    return result


async def handle_info_reviewstr(reviewstr: str | None) -> str | None:
    if reviewstr is None:
        return None
    return reviewstr.replace("<br>", "\n")


async def handle_info(info: dict[str, str]) -> list[str]:
    name = info.get("name")
    release_data = info.get("release")
    store_link = info.get("link")
    reviews = await handle_info_reviewstr(info.get("reviewstr"))
    if reviews is None:
        print("reviews is none")
        pass
    return [name, release_data, store_link, reviews]


async def handle_price(price: str | dict[str, str], price_type: int) -> list[str] | str:
    if price_type == 1:
        percent = price.get("percent")
        orig_price = price.get("price")
        disc_price = price.get("final_price")
        return [percent, orig_price, disc_price]
    return price


async def handle_result(search_term: str):
    result = await search(search_term)
    if result is None:
        return None
    info = await handle_info(result.get("info"))
    price = result.get("price")
    price_type = result.get("price_type")
    handled_price = await handle_price(price, price_type)
    return info, handled_price


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        r = runner.run(handle_result("don't starve together"))
        print(r)
