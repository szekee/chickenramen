from flask import Flask, request
from flask_cors import CORS

# import numpy as np
# import model
# from utils import fe_sk

from utils.take_photo import take_photo

DIRECTORY = "../models"

app = Flask(__name__)
CORS(app)



@app.route("/")
def index():
    return "hi"


@app.route("/tourl", methods=["post"])
def tourl():
    data_obj = request.json

    url = take_photo(data_obj)

    return url



@app.route("/checkurl", methods=["post"])
def check_url():

    url = request.json()

    # extracted_url = fe_sk.feature_extraction(url)
    # extracted = np.array(extracted_url).reshape(-1,8)

    # prediction = models.gbc_model.predict(extracted)
    # print(prediction[0])

    # return {
    #     "prediction": int(prediction[0]),
    # }

    return url


if __name__ == "__main__":
    app.run(debug=True)