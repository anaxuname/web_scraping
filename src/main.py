import config
from models import Product
from time import sleep
import csv

from utils import get_product_info, get_products


def main():
    """
    Main function.
    """
    data = config.json_data
    page = 1
    with open("products.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n", delimiter=";")
        while page <= config.MAX_PAGES:
            data["pageNumber"] = page
            products = get_products(data)
            sleep(config.TIME_TO_SLEEP)
            if products:
                for product in products:
                    p = Product(**product)
                    print(f"{config.base_site_url}{p.url}")
                    product_info = get_product_info(
                        f"{config.base_site_url}{p.url}"
                    )
                    sleep(config.TIME_TO_SLEEP)
                    writer.writerow(
                        [
                            f"{config.base_site_url}{p.url}",
                            p.name,
                            p.price.actual.amount,
                            p.reviews.rating,
                            product_info.description,
                            product_info.instructions,
                            product_info.country,
                        ]
                    )
            else:
                break

            page += 1


if __name__ == "__main__":
    main()
