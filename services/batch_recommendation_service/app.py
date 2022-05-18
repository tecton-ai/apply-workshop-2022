import json
import os
import pickle

from dotenv import load_dotenv
from flask import Flask, abort
from flask_cors import CORS, cross_origin
from urllib3 import PoolManager

load_dotenv()  # take environment variables from .env.

headers = {
    "Authorization": f'Tecton-key {os.environ["TECTON_API_KEY"]}',
}
url = f"https://{os.environ['TECTON_URL']}/api/v1/feature-service/get-features"

movieid2title = pickle.load(open("movieid2title.p", "rb"))
http = PoolManager()

app = Flask(__name__)
CORS(app)


@app.route("/recommendations/<string:user_id>/")
def get_recommendations(user_id):
    data = json.dumps(
        {
            "params": {
                "feature_service_name": os.environ["TECTON_FEATURE_SERVICE"],
                "join_key_map": {
                    "USER_ID": user_id,
                },
                "workspace_name": "apply-2022-demo",
            },
        }
    )
    r = http.request("POST", url=url, headers=headers, body=data)
    movie_ids = json.loads(r.data.decode("utf-8"))["result"]["features"][0].split(",")
    titles = [movieid2title[int(m)] for m in movie_ids]
    return {"movie_ids": movie_ids, "recommended_titles": titles}
