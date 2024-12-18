import redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB, CACHE_TTL


class CacheManager:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

    def is_price_changed(self, product_identifier, product_price):
        cached_price = self.redis_client.get(product_identifier)
        if cached_price and float(cached_price) == product_price:
            return False
        self.redis_client.set(product_identifier, product_price, ex=CACHE_TTL)
        return True

    def clear_cache(self):
        """Clear all cache data."""
        self.redis_client.flushdb()

