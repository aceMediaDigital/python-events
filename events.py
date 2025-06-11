# =======================================================
#
#  Created by anele on 10/06/2025
#
#  @anele_ace
#
# =======================================================

import asyncio
import requests
import nest_asyncio
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession


def get_web_tickets_events(itemid):
    url = "https://www.webtickets.co.za/v2/category.aspx?itemid={itemid}&location=0&when=anytime"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the container div
    events_div = soup.find("div", {"id": "divEvents"})
    if not events_div:
        return {"error": "No events found"}

    # Find all individual event cards inside the div
    event_cards = events_div.find_all("div", {"class": "product-card"})

    events = []
    for card in event_cards:
        title_tag = card.find("h3", class_="product-card-title")
        date_tag = card.find("div", class_="product-card-meta")
        price_tag = card.find("div", class_="product-card-price")
        image_tag = card.find("div", class_="product-card-thumb")
        img = image_tag.find("img") if image_tag else None

        category_ul = card.find("ul", class_="product-card-category")
        category_li = category_ul.find("li") if category_ul else None

        title = title_tag.text.strip() if title_tag else None
        date = date_tag.text.strip() if date_tag else None
        price = price_tag.text.strip() if date_tag else None
        image = img['src'] if img and img.has_attr('src') else None
        venue = category_li.text.strip() if category_li else None

        if title or date:
            events.append({
                "title": title,
                "date": date,
                "price": price,
                "image": image,
                "venue": venue
            })

    return events


async def get_howler_music_events():
    url = "https://www.howler.co.za/categories/17"
    headers = {"User-Agent": "Mozilla/5.0"}
    session = AsyncHTMLSession()

    response = await session.get(url, headers=headers)

    async def render():
        await response.html.arender(sleep=1, timeout=20)

    asyncio.run(render())  # This must be in the main thread

    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    event_cards = response.html.find(".grid__cell")

    events = []
    for card in event_cards:
        title_el = card.find(".upcoming-event-card__title", first=True)
        date_el = card.find(".upcoming-event-card__date", first=True)

        title = title_el.text if title_el else None
        date = date_el.text if date_el else None

        if title or date:
            events.append({
                "title": title,
                "date": date,
            })

    return {"howler": events}


def get_howler_music_events_sync():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # No event loop in this thread, create a new one and set it
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        # Patch to allow nested event loops
        nest_asyncio.apply()
        # Now we can run the async func within existing loop
        return loop.run_until_complete(get_howler_music_events())
    else:
        # Normal case: just run it
        return loop.run_until_complete(get_howler_music_events())

