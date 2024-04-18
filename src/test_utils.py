import unittest
import requests
from unittest.mock import patch

from utils import get_product_info, get_products, make_request


class TestMakeRequest(unittest.TestCase):
    @patch("requests.request")
    def test_make_request_success(self, mock_request):
        mock_request.return_value.status_code = 200

        response = make_request(method="GET", url="https://google.com")

        mock_request.assert_called_once()
        self.assertEqual(response.status_code, 200)

    def test_make_request_raises_error_on_failure(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            make_request(method="DELETE", url="https://google.com")


class TestGetProducts(unittest.TestCase):
    class MockResponse:
        def __init__(self, response):
            self.status_code = 200
            self.response = response

        def json(self):
            return self.response

        def raise_for_status(self):
            """Raise an exception if the response is not successful."""
            pass

    def test_get_products_success(self):
        with patch(
            "utils.make_request",
            return_value=self.MockResponse(
                {
                    "data": {
                        "products": [
                            {"name": "Laptop"},
                            {"name": "Smartphone"},
                        ]
                    }
                }
            ),
        ):
            data = {"query": {"category": "electronics"}}
            expected = [{"name": "Laptop"}, {"name": "Smartphone"}]

            result = get_products(data)
            self.assertEqual(result, expected)

    def test_get_products_no_data(self):
        with patch(
            "utils.make_request",
            return_value=self.MockResponse({"data": {"products": []}}),
        ):
            result = get_products({})

            self.assertEqual(result, [])

    def test_get_products_invalid_response(self):
        with patch(
            "utils.make_request",
            return_value=self.MockResponse({"data": {"products": []}}),
        ):
            result = get_products({})

            self.assertNotIsInstance(result, dict)


class TestGetProductInfo(unittest.TestCase):
    class MockResponse:
        def __init__(self, text):
            self.status_code = 200
            self.text = text

    def test_get_product_info_normal(self):
        url = "http://example.com/product"
        mock_response = "<div itemprop='description'>Product description</div><div text='применение'><div>Product instructions</div></div><div text='Дополнительная информация'><div><br/>Product country</div></div>"

        with patch(
            "utils.make_request", return_value=self.MockResponse(mock_response)
        ):
            product_info = get_product_info(url)
            self.assertEqual(product_info.description, "Product description")
            self.assertEqual(product_info.instructions, "Product instructions")
            self.assertEqual(product_info.country, "Product country")

    def test_get_product_info_missing_fields(self):
        url = "http://example.com/product"
        mock_response = (
            "<div>No description</div><div text='Some other section'></div>"
        )

        with patch(
            "utils.make_request", return_value=self.MockResponse(mock_response)
        ):
            product_info = get_product_info(url)
            self.assertEqual(product_info.description, "")
            self.assertEqual(product_info.instructions, "")
            self.assertEqual(product_info.country, "")

    def test_get_product_info_empty_response(self):
        url = "http://example.com/product"
        mock_response = ""
        with patch(
            "utils.make_request", return_value=self.MockResponse(mock_response)
        ):
            product_info = get_product_info(url)
            self.assertEqual(product_info.description, "")
            self.assertEqual(product_info.instructions, "")
            self.assertEqual(product_info.country, "")


if __name__ == "__main__":
    unittest.main()
