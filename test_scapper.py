import unittest
from scraper import Scraper
from storage import JSONFileStorage
from cache import CacheManager
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
        self.cache = CacheManager()
        self.notifier = MockNotifier()
        self.scraper = Scraper(storage_handler=self.storage, cache_manager=self.cache, notifier=self.notifier)

    def test_scrape_single_page(self):
        # Mock HTML response
        def mock_get(url, headers=None, proxies=None):
            class MockResponse:
                status_code = 200
                def text(self):
                    return """<div class='product-inner'>
                                <h3>Product 1</h3>
                                <span class='woocommerce-Price-amount'>$10.0</span>
                                <a><img src='http://example.com/image1.jpg' title="Product 1"/></a>
                            </div>"""
            return MockResponse()

        requests.get = mock_get
        self.scraper.scrape(max_pages=1)
        self.assertEqual(len(self.storage.data), 1)
        self.assertEqual(self.notifier.message, "Scraping completed. 1 products updated in the database.")

    def test_cache_prevention(self):
        self.cache.is_price_changed("Product 1", 10.0)
        self.assertFalse(self.cache.is_price_changed("Product 1", 10.0))
        self.assertTrue(self.cache.is_price_changed("Product 1", 20.0))

if __name__ == "__main__":
    unittest.main()
