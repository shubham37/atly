import unittest
from unittest.mock import patch, Mock
from scraper import Scraper
from storage import JSONFileStorage
from notifications import ConsoleNotifier
import requests

class MockStorage(JSONFileStorage):
    def __init__(self):
        self.data = []

    def save_product(self, product_data):
        self.data.append(product_data)

class MockNotifier(ConsoleNotifier):
    def __init__(self):
        self.message = ""

    def notify(self, count):
        self.message = f"Scraping completed. {count} products updated in the database."

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.storage = MockStorage()
        self.cache = Mock()
        self.notifier = MockNotifier()
        self.scraper = Scraper(storage_handler=self.storage, cache_manager=self.cache, notifier=self.notifier)


    @patch('scraper.Scraper.download_image', return_value='/tmp/atly_images/image1.jpg')
    def test_scrape_single_page(self, mock_download_image):
        # Mock HTML response
        def mock_get(url, headers=None, proxies=None):
            class MockResponse:
                status_code = 200
                text = """
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Basic HTML Page</title>
                        </head>
                        <body>
                            <div class='product-inner'>
                                <h3>Product 1</h3>
                                <span class='woocommerce-Price-amount'>$10.0</span>
                                <a><img src='http://example.com/image1.jpg' title="Product 1"/></a>
                            </div>
                        </body>
                    </html>
                """
            return MockResponse()

        self.cache.is_price_changed.return_value = True
        requests.get = mock_get
        self.scraper.scrape(max_pages=1)
        self.assertEqual(len(self.storage.data), 1)
        self.assertEqual(self.notifier.message, "Scraping completed. 1 products updated in the database.")


if __name__ == "__main__":
    unittest.main()
