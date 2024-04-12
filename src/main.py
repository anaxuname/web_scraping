import requests
import config
from models import Product


def get_products(data):
    response = requests.post(
        config.site_url,
        headers=config.headers,
        json=data,
    )

    return response.json().get("data", {}).get("products", [])


def main():
    data = config.json_data
    page = 1
    while True:
        data["pageNumber"] = page
        products = get_products(data)
        if products:
            for product in products:
                p = Product(**product)
                # product_info = get_product_info(p.url)
                print(p.url, p.name, p.price.actual.amount, p.reviews.rating)
        else:
            break

        page += 1
    print("Done")


if __name__ == "__main__":
    main()
