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


def get_web_tickets_events():
    url = "https://www.webtickets.co.za/v2/category.aspx?itemid=1184163&location=0&when=anytime"
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


