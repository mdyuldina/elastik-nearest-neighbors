"""
Minimal Flask web app to demonstrate Elasticsearch-Aknn functionality
on corpus of Twitter image features.
"""

from flask import Flask, request, render_template, redirect
from itertools import cycle
from pprint import pprint
import os
import random
import requests

# Get elasticsearch hosts from environment variable.
ESHOSTS = cycle(["http://localhost:9200"])
if "ESHOSTS" in os.environ:
    ESHOSTS = cycle(os.environ["ESHOSTS"].split(","))

# Define a set of images to cycle through for the /demo endpoint.
DEMO_IDS = [
    "202546296",
    "202018851",
    "202578505",
    "202025072",
    "100675694",
    "202565190",
    "202222298",
    "202565523",
    "202578639",
    "100037608",
    "100536507",
    "100628203"
]

app = Flask(__name__)


@app.route("/slides")
def slides():
    return redirect("https://docs.google.com/presentation/d/1AyIyBqzCqKhytZWcQfSEhtBRN-iHUldBQn14MGGKpr8/present",
                    code=302)

@app.route("/")
@app.route("/demo")
def demo():
    return redirect("/rugs/docs/demo", code=302)

@app.route("/<es_index>/<es_type>/<es_id>")
def images(es_index, es_type, es_id):

    # Parse elasticsearch ID. If "demo", pick a random demo image ID.
    if es_id.lower() == "demo":
        es_id = random.choice(DEMO_IDS)

    elif es_id.lower() == "random":
        body = {
            "_source": ["s3_url"],
            "size": 1,
            "query": {
                "function_score": {
                    "query": {"match_all": {}},
                    "boost": 5,
                    "random_score": {},
                    "boost_mode": "multiply"
                }
            }
        }
        req_url = "%s/%s/%s/_search" % (next(ESHOSTS), es_index, es_type)
        req = requests.get(req_url, json=body)
        es_id = req.json()["hits"]["hits"][0]["_id"]

    # Get number of docs in corpus.
    req_url = "%s/%s/%s/_count" % (next(ESHOSTS), es_index, es_type)
    req = requests.get(req_url)
    count = req.json()["count"]

    filter = request.args.get('f', "")
    if filter:
        filter = "&f=" + filter
    req_url = "%s/%s/%s/%s/_aknn_search?k1=100&k2=9%s" % (
        next(ESHOSTS), es_index, es_type, es_id, filter)
    req = requests.get(req_url)
    hits = req.json()["hits"]["hits"]
    took_ms = req.json()["took"]

    searched_imaged_req_url = "%s/%s/%s/%s" % (next(ESHOSTS), es_index, es_type, es_id)
    result = requests.get(searched_imaged_req_url)

    query_img, neighbor_imgs = result.json(), hits[0:]

    # Render template.
    return render_template(
        "index.html",
        es_index=es_index,
        es_type=es_type,
        took_ms=took_ms,
        count=count,
        query_img=query_img,
        neighbor_imgs=neighbor_imgs)
