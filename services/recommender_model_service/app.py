import base64
import pickle
import time
from copy import deepcopy

import numpy as np
import pandas as pd
from flask import Flask, abort, request
from pytorch_tabnet.tab_model import TabNetRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class TabNetInference(object):
    def __init__(self, model_path, schema_path, encoder_path):
        self.l_encs = pickle.load(open(encoder_path, "rb"))
        self.schema = pickle.load(open(schema_path, "rb"))

        self.model = TabNetRegressor()
        self.model.load_model(model_path)

    def preprocess(self, df):
        categorical_columns = ["USER_ID", "MOVIE_ID"]
        for col in self.l_encs:
            l_enc = self.l_encs[col]
            df[col] = l_enc.transform(df[col].values)
        df = df[self.schema].fillna(-1)
        return df.values

    def predict(self, df):
        x = self.preprocess(df)
        preds = self.model.predict(x).flatten().tolist()
        return preds


model = TabNetInference(
    "model/batch_movie_recommender_5_6.zip", "model/schema.p", "model/encoders.p"
)
app = Flask(__name__)

start = time.time()


@app.route("/predict/", methods=["POST"])
def get_predicted_rating():
    content = request.get_json(silent=True)
    df = pickle.loads(base64.b64decode(content["df"].encode()))
    preds = model.predict(df)
    return {"predictions": preds}
