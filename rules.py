import re
import urllib.parse
from difflib import SequenceMatcher
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update",
    "account", "bank", "confirm", "free", "gift"
]

def has_ip_address(url):
    return bool(re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', url))

def url_length_check(url):
    return len(url) > 75

def count_subdomains(url):
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc
    return domain.count('.') > 3

def contains_unicode(url):
    try:
        url.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True

def contains_suspicious_keywords(url):
    return any(word in url.lower() for word in SUSPICIOUS_KEYWORDS)
TRUSTED_DOMAINS = [
    "google.com",
    "amazon.com",
    "facebook.com",
    "paypal.com",
    "microsoft.com",
    "apple.com"
]

def is_typosquatting(domain):
    for legit in TRUSTED_DOMAINS:
        ratio = SequenceMatcher(None, domain, legit).ratio()
        if ratio > 0.85 and domain != legit:
            return True
    return False


def rule_based_check(url):
    flags = []

    if has_ip_address(url):
        flags.append("IP address in URL")

    if url_length_check(url):
        flags.append("Very long URL")

    if count_subdomains(url):
        flags.append("Too many subdomains")

    if contains_unicode(url):
        flags.append("Unicode / homograph attack")

    if contains_suspicious_keywords(url):
        flags.append("Suspicious keywords")

    # 🔥 Typosquatting check (single-letter attack)
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")

    if domain and is_typosquatting(domain):
        flags.append("Possible typosquatting attack")

    return flags
