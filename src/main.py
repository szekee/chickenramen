import pickle
from flask import Flask, request, render_template

import numpy as np
from utils import fe_sk
from tensorflow import keras

app = Flask(__name__)

lstm_model = keras.models.load_model("models/lstm")
xgb_model = pickle.load(open("models/xgb.pkl", "rb"))
gbc_model = pickle.load(open("models/gbc.pkl", "rb"))
mlp_model = pickle.load(open("models/mlp.pkl", "rb"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/checkurl", methods=["post"])
def check_url():

    url = request.form['url']

    extracted_url = fe_sk.feature_extraction(url)
    extracted = np.array(extracted_url).reshape(-1,8)

    prediction = gbc_model.predict(extracted)
    print(prediction[0])

    return {
        "prediction": int(prediction[0]),
    }


if __name__ == "__main__":
    app.run(debug=True)