import re
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)

    features = {
        "url_length": len(url),
        "has_https": 1 if parsed.scheme == "https" else 0,
        "count_dots": url.count("."),
        "count_hyphens": url.count("-"),
        "count_at": url.count("@"),
        "count_question": url.count("?"),
        "count_equal": url.count("="),
        "count_slash": url.count("/"),
        "count_digits": sum(char.isdigit() for char in url),
        "count_letters": sum(char.isalpha() for char in url),
    }

    return features