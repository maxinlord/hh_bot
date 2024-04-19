

def filter_by_keys(d: dict, keys: list):
    return {k: d[k] for k in keys if k in d}