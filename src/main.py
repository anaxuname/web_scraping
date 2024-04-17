import config
from models import Product
import csv

from utils import get_product_info, get_products


def main():
    data = config.json_data
    page = 1
    with open("products.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n", delimiter=";")
        while page < 2:
            data["pageNumber"] = page
            products = get_products(data)
            if products:
                for product in products:
                    p = Product(**product)
                    print(f"{config.base_site_url}{p.url}")
                    product_info = get_product_info(
                        f"{config.base_site_url}{p.url}"
                    )
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
    print("Done")


if __name__ == "__main__":
    main()
