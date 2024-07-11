from cachetools import cached, TTLCache

text_cache = TTLCache(maxsize=200, ttl=1000)
button_cache = TTLCache(maxsize=100, ttl=1500)