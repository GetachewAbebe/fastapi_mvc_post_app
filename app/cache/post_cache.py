from cachetools import TTLCache

post_cache = TTLCache(maxsize=1000, ttl=300)  # 5 min TTL
