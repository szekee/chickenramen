import nltk
nltk.download('punkt')
import tldextract
import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse
from nltk.util import ngrams
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import csr_matrix

#Using IP Addresses within Address Bar
def isIPAddress(url):
    # declaring the regex pattern for IP addresses
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    if (pattern.search(url)):
        return 1
    return 0

#Long URL (Characters)
def urlLength(url):
    return len(url)

#URL with @ Symbol
def hasAt(url):
    if '@' in url:
        return 1
    return 0

#URL with multiple "//" for redirecting
def hasDoubleSlash(url):
    if '//' in url:
        return 1
    return 0

#URL Domain with - Symbol
def hasDash(url):
    if '-' in url.split('.')[0]:
        return 1
    return 0

#URL with multiple "." for subdomains
def hasMultipleDots(url):
    if '.' in url:
        return 1
    return 0

#URL with "?"
def hasQuestion(url):
    if '?' in url:
        return 1
    return 0

#URL with "cmd"
def hasCmd(url):
    if 'cmd' in url:
        return 1
    return 0

#URL with ".php"
def hasPhp(url):
    if '.php' in url:
        return 1
    return 0

#URL with HTTPS in domain
def hasHTTPorHTTPS(url):
    if 'http' in url:
        return 1
    return 0

#Total Digits Domain
def digitsDomain(url):
    return len(re.sub("[^0-9]", "", url.split("/", 1)[0]))

#Total Digits Path
def digitsPath(url):
    if len(url.split("/", 1)) == 2:
        return len(re.sub("[^0-9]", "", url.split("/", 1)[1]))
    return 0

def generate_url_ngrams(n: int, url: str):
    url_formated = ''
    
    for index, char in enumerate(url):
        if index % n == 0:
            url_formated += ' '
        url_formated += char

    ngram = ngrams(sequence=nltk.word_tokenize(url_formated), n=n)
    
    ngram_url = {}
    for grams in ngram:
        for gx in grams:
            ngram_url[gx] = 1
    return ngram_url


def get_fields_url(url: str):
    try:
        features = dict()

        url_tldextract = tldextract.extract(url) 
        url_urlparse = urlparse(f"http://{url}")
        url_info = [
            {"name": "domain", "string": url_tldextract.domain},
            {"name": "subdomain", "string": url_tldextract.subdomain},
            {"name": "suffix", "string": url_tldextract.suffix},
            {"name": "path", "string": url_urlparse.path},
            {"name": "params", "string": url_urlparse.params},
            {"name": "query", "string": url_urlparse.query},
            {"name": "fragment", "string": url_urlparse.fragment}
        ]
        features.update(generate_url_ngrams(2, url_tldextract.domain))
        
        for each_url in url_info:
            features[f'len_{each_url["name"]}'] = len(each_url["string"])
            for char_ in list(map(str, "-@_?=&./,")):
                features[f'char{char_}-{each_url["name"]}'] = each_url["string"].count(char_)

            if "domain" == each_url["name"] or "path" == each_url["name"]:
                total_letter, total_number = 0, 0
                for char_ in list(map(str, "abcdefghijklmnopqrstuvwxyz")):
                    total_letter += each_url["string"].lower().count(char_)

                for char_ in list(map(str, "0123456789")):
                    total_number += each_url["string"].lower().count(char_)

                features[f'letter_len_{each_url["name"]}'] = total_letter
                features[f'number_len_{each_url["name"]}'] = total_number
    except Exception as e:
        return e      
    return features   

def get_features(url):
    if "http://" == url[:7]:
        url = url[7:]
    elif "https://" == url[:8]:
        url = url[8:]
    features_json = {}
    features_json = get_fields_url(url)
    features_json['ip_addr'] = isIPAddress(url)
    features_json['url_len'] = urlLength(url)
    features_json['has_at'] = hasAt(url)
    features_json['has_double_slash'] = hasDoubleSlash(url)
    features_json['has_dash'] = hasDash(url)
    features_json['has_multiple_dots'] = hasMultipleDots(url)
    features_json['has_question_mark'] = hasQuestion(url)
    features_json['has_cmd'] = hasCmd(url)
    features_json['has_php'] = hasPhp(url)
    features_json['has_http'] = hasHTTPorHTTPS(url)
    features_json['digits_domain'] = digitsDomain(url)
    features_json['digits_path'] = digitsPath(url)
    return features_json

def feature_to_vector(features_json, pre_processor):   
    X = pre_processor.transform([features_json])
    X = csr_matrix(X)
    X = X.tocsr()
    return X

def get_prediction(vector, lg, xgb, rfc, nn):
    if nn.predict(vector) == 1:
        nn_pred = 1
    else:
        nn_pred = 0
    if lg.predict(vector)+xgb.predict(vector)+rfc.predict(vector)+nn_pred > 2:
        return 1
    return 0

def url_phishing_predictor_js(url, pre_processor, lg, xgb, rfc, nn):
    return get_prediction(feature_to_vector(get_features(url), pre_processor), lg, xgb, rfc, nn)