import sys


sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

json_data = {
    "categoryId": 1000000007,
    "cityId": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
    "filters": [],
}

base_site_url = "https://goldapple.ru"

site_url = base_site_url + "/front/api/catalog/products"


MAX_PAGES = 1

TIME_TO_SLEEP = 4
