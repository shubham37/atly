
import os
import requests
from bs4 import BeautifulSoup

from config import IMAGE_DIR
from storage import StorageHandler
from cache import CacheManager
from notifications import Notifier
from utils import generate_slug


class Scraper:
    def __init__(self, storage_handler: StorageHandler, cache_manager: CacheManager, notifier: Notifier):
        self.storage_handler = storage_handler
        self.cache_manager = cache_manager
        self.notifier = notifier

    def scrape(self, max_pages: int = None, proxy: str = None):
        base_url = "https://dentalstall.com/shop/"
        page = 1
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": proxy, "https": proxy} if proxy else None

        scraped_count = 0
        while True:
            if max_pages and page > max_pages:
                break

            url = f"{base_url}?page={page}"
            response = requests.get(url, headers=headers, proxies=proxies)

            if response.status_code != 200:
                print(f"Failed to fetch page {page}, retrying...")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all("div", class_="product-inner")

            if not products:
                break

            for product in products:
                title = product.find('a').find('img').get('title').strip()
                unique_identifier = generate_slug(title)

                prices =  product.findAll("span", class_="woocommerce-Price-amount")
                current_price = float(prices[0].text.strip().replace("$", "").replace("₹", ""))

                image_url = product.find('a').find('img')["src"]
                image_path = self.download_image(image_url)

                if not self.cache_manager.is_price_changed(unique_identifier, current_price):
                    continue

                self.storage_handler.save_product({
                    "product_title": title,
                    "product_price": current_price,
                    "path_to_image": image_path,
                })
                scraped_count += 1

            page += 1

        self.notifier.notify(scraped_count)

    def download_image(self, url):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            image_name = url.split("/")[-1]
            if not os.path.exists(IMAGE_DIR):
                os.makedirs(IMAGE_DIR)
            image_path = os.path.join(IMAGE_DIR, image_name)
            with open(image_path, "wb") as file:
                for chunk in response:
                    file.write(chunk)
            return image_path
