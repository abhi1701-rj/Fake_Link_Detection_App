import re
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)

    return [
        len(url),                          # url_length
        int(parsed.scheme == "https"),     # has_https
        int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),  # has_ip
        int("@" in url),                   # has_at
        url.count("."),                    # dot_count
        sum(c.isdigit() for c in url),     # digit_count
        int("-" in parsed.netloc),          # has_hyphen
        int(any(s in url for s in ["bit.ly", "tinyurl", "t.co"]))  # shortened
    ]
