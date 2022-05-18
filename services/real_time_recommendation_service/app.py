import asyncio
import base64
import json
import os
import pickle
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from functools import lru_cache

import aiohttp
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, abort
from flask_cors import CORS, cross_origin
from urllib3 import HTTPConnectionPool, HTTPSConnectionPool

load_dotenv()  # take environment variables from .env.

auth_headers = {
    "Authorization": f'Tecton-key {os.environ["TECTON_API_KEY"]}',
}
prediction_headers = {"Content-Type": "application/json"}

endpoint = "/api/v1/feature-service/get-features"
tecton_conn_pool = HTTPSConnectionPool(os.environ["TECTON_URL"])
prediction_conn_pool = HTTPConnectionPool("localhost:5002")
loop = asyncio.new_event_loop()
connector = aiohttp.TCPConnector(limit=100, loop=loop)
client = aiohttp.ClientSession(loop=loop, headers=auth_headers, connector=connector)
url = f"https://{os.environ['TECTON_URL']}/api/v1/feature-service/get-features"

movieid2title = pickle.load(open("movieid2title.p", "rb"))

app = Flask(__name__)
CORS(app)

def get_schema():
    data = json.dumps(
        {
            "params": {
                "feature_service_name": os.environ["TECTON_FEATURE_SERVICE"],
                "join_key_map": {
                    "USER_ID": "1",
                    "MOVIE_ID": "1",
                },
                "workspace_name": "apply-2022-demo",
                "metadata_options": {"include_names": True, "include_data_types": True},
            },
        }
    )
    r = tecton_conn_pool.request("POST", url=endpoint, headers=auth_headers, body=data)
    data = json.loads(r.data.decode("utf-8"))["metadata"]["features"]
    names = ["USER_ID", "MOVIE_ID"] + [f["name"] for f in data]
    names = [n.upper().replace(".", "__") for n in names]
    types = ["string", "string"] + [f["dataType"]["type"] for f in data]
    return names, types


names, types = get_schema()


def generate_candidates(movie_id):
    data = json.dumps(
        {
            "params": {
                "feature_service_name": os.environ["TECTON_NEAREST_NEIGHBOR_SERVICE"],
                "join_key_map": {
                    "MOVIE_ID": movie_id,
                },
                "workspace_name": "apply-2022-demo",
            },
        }
    )
    r = tecton_conn_pool.request("POST", url=endpoint, headers=auth_headers, body=data)
    candidates = json.loads(r.data.decode("utf-8"))["result"]["features"][0].split(",")[
        1:
    ]
    return candidates


def get_predictions(df):
    dfs = pickle.dumps(df)
    dfs = base64.b64encode(dfs).decode("utf-8")
    r = prediction_conn_pool.request(
        "POST",
        url="/predict/",
        headers=prediction_headers,
        body=json.dumps({"df": dfs}),
    )
    return r.data.decode("utf-8")


async def get_feature_vector(user_id, movie_id):
    data = json.dumps(
        {
            "params": {
                "feature_service_name": os.environ["TECTON_FEATURE_SERVICE"],
                "join_key_map": {
                    "USER_ID": user_id,
                    "MOVIE_ID": movie_id,
                },
                "workspace_name": "apply-2022-demo",
            },
        }
    )
    async with client.post(url=url, headers=auth_headers, data=data) as response:
        resp = await response.read()
        fv = json.loads(resp.decode("utf-8"))
        if "result" in fv:
            return [user_id, movie_id] + fv["result"]["features"]
        return None


async def get_feature_vectors(user_id, movie_ids):
    tasks = [get_feature_vector(user_id, movie_id) for movie_id in movie_ids]
    feature_vectors = await asyncio.gather(*tasks)
    return feature_vectors


def filter_candidates(user_id, movie_ids):
    data = json.dumps(
        {
            "params": {
                "feature_service_name": os.environ["TECTON_RECENTLY_WATCHED_SERVICE"],
                "join_key_map": {
                    "USER_ID": user_id,
                },
                "workspace_name": "apply-2022-demo",
            },
        }
    )
    r = tecton_conn_pool.request("POST", url=endpoint, headers=auth_headers, body=data)
    recently_watched = json.loads(r.data.decode("utf-8"))["result"]["features"][0]
    print(recently_watched)
    if recently_watched is None:
        return movie_ids
    else:
        print(recently_watched.split(","))
        filtered = list(set(movie_ids) - set(recently_watched.split(",")))
        return filtered


def rank_candidates(user_id, movie_ids):
    start = time.time()
    fvs = loop.run_until_complete(get_feature_vectors(user_id, movie_ids))
    feature_lookup_time = time.time() - start
    print(f"Feature lookup time: {feature_lookup_time}")
    # create feature dataframe
    feature_vectors = [fv for fv in fvs if fv]
    df = pd.DataFrame(feature_vectors, columns=names)

    # Apply correct schema and typing
    for i, col in enumerate(df.columns):
        df[col] = df[col].astype(types[i])

    # Call prediction endpoint
    preds = json.loads(get_predictions(df))["predictions"]

    # Sort by predicted rating
    preds_and_ids = sorted(
        [(p, r) for p, r in zip(preds, list(df.MOVIE_ID.values))],
        key=lambda x: x[0],
        reverse=True,
    )
    return preds_and_ids


@lru_cache
def _get_recommendations(user_id, movie_id, date):
    movie_ids = generate_candidates(movie_id)
    filtered_movie_ids = filter_candidates(user_id, movie_ids)
    preds_and_ids = rank_candidates(user_id, filtered_movie_ids)
    
    recommended_titles = [movieid2title[int(id)] for _, id in preds_and_ids]
    titles_and_scores = [(movieid2title[int(id)], p) for p, id in preds_and_ids]
    return {
        "predicted_scores":titles_and_scores,
        "recommended_ids": [id for _, id in preds_and_ids],
        "recommended_titles": recommended_titles,
    }


@app.route("/recommend-next/<string:user_id>/<string:movie_id>/")
def get_recommendation(user_id, movie_id):
    start = time.time()
    recommendations = _get_recommendations(user_id, movie_id, date.today())
    recommendation_time = time.time() - start
    recommendations["time_taken"] = recommendation_time
    return recommendations
