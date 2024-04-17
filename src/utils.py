import requests
import config
from bs4 import BeautifulSoup

from models import ProductInfo


def make_request(**kwargs):
    response = requests.request(headers=config.headers, **kwargs)
    response.raise_for_status()

    return response


def get_products(data):
    response = make_request(
        method="POST",
        url=config.site_url,
        json=data,
    )

    return response.json().get("data", {}).get("products", [])


def get_product_info(url):
    response = make_request(method="GET", url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.find("div", {"itemprop": "description"})
    instructions = soup.find("div", {"text": "применение"})
    if instructions:
        instructions = instructions.find("div").text.rstrip()
    else:
        instructions = ""
    country = soup.find("div", {"text": "Дополнительная информация"})
    if country:
        country = country.find("div").decode_contents().split("<br/>")[1]
    else:
        country = ""

    return ProductInfo(
        description=description.text,
        instructions=instructions,
        country=country,
    )
