import ipaddress
from urllib.parse import urlparse
import regex as re


def use_https(url):
    if url.startswith("https"):
        return 1
    return 0

def has_ip(url):
    domain = urlparse(url).netloc
    try:
        ipaddress.ip_address(domain)
        return 1
    except:
        return 0

def length_of_url(url):
    return len(url)

def symbols_to_totalch(url):
    if len(url) == 0:
        return None
    num_symbols = len(url)-len(re.findall('[\w]', url))
    return round(num_symbols / len(url), 5)

def have_at(url):
    if "@" in url:
        return 1    
    return 0 

def have_redirection(url):
    position = url.rfind("//")
    if position > 7:
        return 1
    return 0

def path_to_url_length(url):
    if len(url) == 0:
        return None

    paths = 0
    url_list = urlparse(url).path.split("/")

    for s in url_list:
        if len(s) != 0:
            paths += 1

    return round(paths / len(url), 5)

def subdomains(url):
    domain = urlparse(url).netloc
    return len(domain.split("."))

def feature_extraction(url):

    url_feature = [
        use_https(url),
        has_ip(url),
        length_of_url(url),
        symbols_to_totalch(url),
        have_at(url),
        have_redirection(url),
        path_to_url_length(url),
        subdomains(url)
    ]

    return url_feature