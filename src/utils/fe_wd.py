import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from nltk.tokenize import RegexpTokenizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

class Converter(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, data_frame):
        return data_frame.values.ravel()

numeric_features = ['length', 'domain_hyphens', 'domain_underscores', 'path_hyphens', 'path_underscores', 'slashes', 'full_stops', 'num_subdomains']
numeric_transformer = Pipeline(steps=[
    ('scaler', MinMaxScaler())])

categorical_features = ['tld', 'is_ip']
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

vectorizer_features = ['domain_tokens','path_tokens']
vectorizer_transformer = Pipeline(steps=[
    ('con', Converter()),
    ('tf', TfidfVectorizer())])

vectorizer_features = ['domain_tokens','path_tokens']
vectorizer_transformer = Pipeline(steps=[
    ('con', Converter()),
    ('tf', TfidfVectorizer())])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('domvec', vectorizer_transformer, ['domain_tokens']),
        ('pathvec', vectorizer_transformer, ['path_tokens'])
    ])

svc_clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LinearSVC())])

log_clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression())])

nb_clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', MultinomialNB())])


tokenizer = RegexpTokenizer(r'[A-Za-z]+')
def tokenize_domain(netloc: str) -> str:
    split_domain = tldextract.extract(netloc)
    no_tld = str(split_domain.subdomain +'.'+ split_domain.domain)
    return " ".join(map(str,tokenizer.tokenize(no_tld)))

def get_num_subdomains(netloc: str) -> int:
    subdomain = tldextract.extract(netloc).subdomain 
    if subdomain == "":
        return 0
    return subdomain.count('.') + 1

def parse_url(url: str): #Optional[Dict[str, str]] --> Saw this online, but not too sure what this is
    try:
        no_scheme = not url.startswith('https://') and not url.startswith('http://')
        if no_scheme:
            parsed_url = urlparse(f"http://{url}")
            return {
                "scheme": None, #No established value for this --> Think this is for http or https
                "netloc": parsed_url.netloc,
                "path": parsed_url.path,
                "params": parsed_url.params,
                "query": parsed_url.query,
                "fragment": parsed_url.fragment,
            }
        else:
            parsed_url = urlparse(url)
            return {
                "scheme": parsed_url.scheme,
                "netloc": parsed_url.netloc,
                "path": parsed_url.path,
                "params": parsed_url.params,
                "query": parsed_url.query,
                "fragment": parsed_url.fragment,
            }
    except:
        return None

def feature_as_input(link):
    link_df = {'url': [link]}
    df_grp = pd.DataFrame(link_df)        
    df_grp["parsed_url"] = df_grp.url.apply(parse_url)
    df_grp = pd.concat([
        df_grp.drop(['parsed_url'], axis=1),
        df_grp['parsed_url'].apply(pd.Series)
    ], axis=1)
    df_grp = df_grp[~df_grp.netloc.isnull()]
    df_grp["length"] = df_grp.url.str.len()
    df_grp["tld"] = df_grp.netloc.apply(lambda nl: tldextract.extract(nl).suffix)
    df_grp['tld'] = df_grp['tld'].replace('','None')
    df_grp["is_ip"] = df_grp.netloc.str.fullmatch(r"\d+\.\d+\.\d+\.\d+")
    df_grp['domain_hyphens'] = df_grp.netloc.str.count('-')
    df_grp['domain_underscores'] = df_grp.netloc.str.count('_')
    df_grp['path_hyphens'] = df_grp.path.str.count('-')
    df_grp['path_underscores'] = df_grp.path.str.count('_')
    df_grp['slashes'] = df_grp.path.str.count('/')
    df_grp['full_stops'] = df_grp.path.str.count('.')
    df_grp['num_subdomains'] = df_grp['netloc'].apply(lambda net: get_num_subdomains(net))        
    df_grp['domain_tokens'] = df_grp['netloc'].apply(lambda net: tokenize_domain(net))
    df_grp['path_tokens'] = df_grp['path'].apply(lambda path: " ".join(map(str,tokenizer.tokenize(path))))

    df_grp.drop('url', axis=1, inplace=True)
    df_grp.drop('scheme', axis=1, inplace=True)
    df_grp.drop('netloc', axis=1, inplace=True)
    df_grp.drop('path', axis=1, inplace=True)
    df_grp.drop('params', axis=1, inplace=True)
    df_grp.drop('query', axis=1, inplace=True)
    df_grp.drop('fragment', axis=1, inplace=True)

    return df_grp.iloc[:, :12]

def url_phishing_predictor_wd(link, lr, svc, nb):
    features = feature_as_input(link)
    if (int(lr.predict(features)[0]) + int(svc.predict(features)[0]) + int(nb.predict(features)[0]) >= 2):
        return 1
    return 0