import requests
import config
from bs4 import BeautifulSoup

from models import ProductInfo


def make_request(**kwargs):
    """
    Makes a request using the provided keyword arguments.

    Args:
        **kwargs: Keyword arguments to be passed to `requests.request`.

    Returns:
        requests.Response: The response object representing the request.

    Raises:
        requests.exceptions.HTTPError: If the response status code is not successful.
    """
    response = requests.request(**kwargs)
    response.raise_for_status()

    return response


def get_products(data):
    """
    Retrieves a list of products from the API using the provided data.

    Args:
        data (dict): The data to be sent in the API request.

    Returns:
        list: A list of products retrieved from the API response. If the API response does not contain a "data" key or the "products" key within the "data" key, an empty list is returned.
    """
    response = make_request(
        method="POST",
        url=config.site_url,
        json=data,
        headers=config.headers,
    )

    return response.json().get("data", {}).get("products", [])


def get_product_info(url):
    """
    Retrieves product information from a given URL.

    Args:
        url (str): The URL of the product page.

    Returns:
        ProductInfo: An object containing the product's description, instructions, and country of origin.
    """
    response = make_request(method="GET", url=url, headers=None)
    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.find("div", {"itemprop": "description"})
    description = (
        description.decode_contents().replace("\n", " ") if description else ""
    )

    instructions = soup.find("div", {"text": "применение"})
    instructions = (
        instructions.find("div").text.rstrip() if instructions else ""
    )

    country = soup.find("div", {"text": "Дополнительная информация"})
    country = (
        country.find("div").decode_contents().split("<br/>")[1]
        if country
        else ""
    )

    return ProductInfo(
        description=description,
        instructions=instructions,
        country=country,
    )
