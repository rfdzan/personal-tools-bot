import asyncio

from bs4 import BeautifulSoup, NavigableString

from .get_request import main as get_page


async def is_discounted(tag) -> dict[str, str]:
    child_price_class_attribute = "discount_block search_discount_block"
    parent_discount = tag.find("div", {"class": child_price_class_attribute})
    discount_percent = parent_discount.find("div", {"class": "discount_pct"}).text
    original_price = parent_discount.find(
        "div", {"class": "discount_original_price"}
    ).text
    discounted_price = parent_discount.find(
        "div", {"class": "discount_final_price"}
    ).text

    return {
        "percent": discount_percent,
        "price": f"~~{original_price}~~",
        "final_price": discounted_price,
    }


async def start_of_parser(search: str) -> NavigableString | None:
    page = await get_page(search)
    soup = BeautifulSoup(page, "lxml")
    div = soup.find("div", {"id": "search_result_container"})
    div2 = div.find("div", {"data-panel": True, "id": True})

    if div2 is None:
        return None

    return div2


async def main_info(div2: NavigableString) -> tuple[NavigableString, dict[str, str]]:
    a = div2.find("a")
    store_link = a.get("href")

    parent_container = a.find("div", {"class": "responsive_search_name_combined"})
    namediv = parent_container.find("div", {"class": "col search_name ellipsis"})
    product_name = namediv.find("span", {"class": "title"}).text
    release_date = parent_container.find(
        "div", {"class": "col search_released responsive_secondrow"}
    ).text
    reviewscore = parent_container.find(
        "div", {"class": "col search_reviewscore responsive_secondrow"}
    )
    review_data = reviewscore.find("span", {"class": True, "data-tooltip-html": True})
    reviews = "No review data found."

    if review_data is not None:
        reviews = review_data.get("data-tooltip-html")

    return parent_container, {
        "name": product_name,
        "release": release_date,
        "link": store_link,
        "reviewstr": reviews,
    }


async def prices(parent_container: NavigableString) -> tuple[str | dict[str, str], int]:
    parent_price = parent_container.find(
        "div", {"class": "col search_price_discount_combined responsive_secondrow"}
    )
    child_price = parent_price.find(
        "div",
        {
            "class": True,
            "data-price-final": True,
            "data-bundlediscount": True,
            "data-discount": True,
        },
    )

    if child_price is None:  # game is Free
        free = parent_price.find("div", {"class": "discount_final_price free"}).text
        return free, 0
    elif child_price.get("data-discount") != "0":  # game is discounted
        discount_data = await is_discounted(parent_price)
        return discount_data, 1
    else:  # regular price
        original_price = parent_price.find(
            "div", {"class": "discount_final_price"}
        ).text
        return original_price, 2


async def main(search: str):
    main_search_page = await start_of_parser(search)

    if main_search_page is None:
        return None

    container_page, product_info = await main_info(main_search_page)
    prices_data, price_type = await prices(container_page)
    return {"info": product_info, "price": prices_data, "price_type": price_type}


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main("don't starve together"))
