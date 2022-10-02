from utils.fe_js import url_phishing_predictor_js
from utils.fe_wd import url_phishing_predictor_wd
from utils.fe_jl import url_phishing_predictor_jl
from utils.fe_hx import url_phishing_predictor_hx

from keras.models import load_model
import joblib
import pickle

dir = "models/"

#JS
rf_imported_js = joblib.load(dir+"RandomForest")
lg_imported_js = joblib.load(dir+"LogisticRegression")
xgb_imported_js = joblib.load(dir+"XGBoost")
nn_imported_js = load_model(dir+"NeuralNet.h5")
pre_processor_imported_js = joblib.load(dir+"Preprocessor")

#JL
DT_imported_jl = joblib.load(dir+"DT")
RF_imported_jl = joblib.load(dir+"RF")
ET_imported_jl = joblib.load(dir+"ET")

#WD
LR_imported_wd = joblib.load(dir+"LR_WD")
SVC_imported_wd = joblib.load(dir+"SVC_WD")
NB_imported_wd = joblib.load(dir+"NB_WD")

#HX
XGB_imported_hx = joblib.load(dir+"XGBoostClassifierNew")

print(url_phishing_predictor_js("https://wikipedia.com", pre_processor_imported_js, lg_imported_js, xgb_imported_js, rf_imported_js, nn_imported_js))
print(url_phishing_predictor_wd("https://wikipedia.com", LR_imported_wd, SVC_imported_wd, NB_imported_wd))
print(url_phishing_predictor_jl("https://wikipedia.com", DT_imported_jl, RF_imported_jl, ET_imported_jl))
print(url_phishing_predictor_hx("https://wikipedia.com", XGB_imported_hx))

#SK
# lstm_model = keras.models.load_model("models/lstm")
xgb_model = pickle.load(open(dir+"xgb.pkl", "rb"))
gbc_model = pickle.load(open(dir+"gbc.pkl", "rb"))
mlp_model = pickle.load(open(dir+"mlp.pkl", "rb"))