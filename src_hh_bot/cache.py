from cachetools import cached, TTLCache

text_cache = TTLCache(maxsize=200, ttl=5)
button_cache = TTLCache(maxsize=100, ttl=5)