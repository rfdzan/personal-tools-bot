import asyncio
import json
import re

import httpx


async def get_response(search: str):
    url = "https://gql.tokopedia.com/graphql/SearchProductQueryV4"
    url_search = search.replace(" ", "%20")
    params_variable = f"device=desktop&navsource=home&ob=23&page=1&q={url_search}&related=true&rows=200&safe_search=false&scheme=https&shipping=&source=universe&srp_component_id=02.02.01.01&st=product&start=1&topads_bucket=true&unique_id=eed752ecfb0e5f990b775881693ed5af&user_addressId=&user_cityId=176&user_districtId=2274&user_id=&user_lat=&user_long=&user_postCode=&user_warehouseId=12210375&variants=&warehouses=12210375%232h%2C0%2315m"  # noqa: E501
    payload = {
        "operationName": "SearchProductQueryV4",
        "variables": {"params": params_variable},
        "query": "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      componentId\n      __typename\n    }\n    data {\n      banner {\n        position\n        text\n        imageUrl\n        url\n        componentId\n        trackingOption\n        __typename\n      }\n      backendFilters\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        componentId\n        trackingOption\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        position\n        trackingOption\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              adsId: id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            badges {\n              title\n              imageUrl\n              show\n              __typename\n            }\n            ratingAverage\n            labelGroups {\n              position\n              type\n              title\n              url\n              __typename\n            }\n            componentId\n            __typename\n          }\n          componentId\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        componentId\n        trackingOption\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          adsId: id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        customVideoURL\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          url\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        ratingAverage\n        shop {\n          shopId: id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",  # noqa: E501
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",  # noqa: E501
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": f"https://www.tokopedia.com/search?navsource=home&page=2&q={url_search}&source=universe&srp_component_id=02.02.01.01&st=product",
        "X-Tkpd-Lite-Service": "zeus",
        "X-Version": "8d4c18e",
        "content-type": "application/json",
        "x-device": "desktop-0.0",
        "Tkpd-UserId": "0",
        "X-Source": "tokopedia-lite",
        "Origin": "https://www.tokopedia.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
    }
    async with httpx.AsyncClient(headers=headers) as session:
        r = await session.post(url, data=payload)
    return r.text
    # with open("response.json", "w") as file:
    #     file.write(r.text)


async def cleanup_sold(sold: str):
    pattern = r"(\d+)(.+)"
    matches = re.match(pattern, sold)
    if matches is None:
        return None
    split = [int(matches.group(1)), matches.group(2)]
    return split


async def get_data(search: str):
    r = json.loads(await get_response(search))[0]
    # with open("response.json") as file:
    #     r = json.loads(file.read())[0]
    raw = r.get("data")
    searchv4 = raw.get("ace_search_product_v4")
    data = searchv4.get("data")
    products = data.get("products")
    listing = []
    for product in products:
        _name = product.get("name")
        badge = product.get("badges")
        if len(badge) > 0:
            _store_badge = badge[0].get("title")
        else:
            _store_badge = "None"
        labelGroups = product.get("labelGroups")
        for info in labelGroups:
            if info.get("position") == "integrity":
                sold = info.get("title") if info is not None else None
        _sold = await cleanup_sold(sold)
        _price = product.get("price")
        _avg_rating = product.get("ratingAverage")
        _url = product.get("url")
        listing.append(
            {
                "name": _name,
                "store_badge": _store_badge,
                "sold": _sold,
                "price": _price,
                "product_rating": _avg_rating,
                "product_url": _url,
            }
        )
    return listing


async def cleanup_data(listing: list[dict]):
    has_rb = []
    has_plus = []
    plain_terjual = []
    for product in listing:  # listing is a list[dict[str, str]]
        if product is None:
            continue
        product_sold_text = product.get("sold")[1]
        if "rb+" in product_sold_text:
            has_rb.append(product)
        elif "+" in product_sold_text:
            has_plus.append(product)
        else:
            plain_terjual.append(product)
    sorted_has_rb = sorted(has_rb, key=lambda x: x.get("sold")[0], reverse=True)
    sorted_has_plus = sorted(has_plus, key=lambda x: x.get("sold")[0], reverse=True)
    sorted_plain_terjual = sorted(
        plain_terjual, key=lambda x: x.get("sold")[0], reverse=True
    )

    sorted_list = sorted_has_rb + sorted_has_plus + sorted_plain_terjual
    return sorted_list


async def prep_dc(search):
    results = await main(search)
    display = []
    for result in results:
        result_prep = []
        for value in result.values():
            if isinstance(value, list):
                value1, value2 = value
                joined_value = "".join([str(value1), value2])
                result_prep.append(joined_value)
                continue
            result_prep.append(value)
        display.append(result_prep)
    return display


async def main(search: str) -> list[dict]:
    listing = await get_data(search)
    result = await cleanup_data(listing)
    return result


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        print(runner.run(prep_dc("Sandisk 64GB SDXC")))
