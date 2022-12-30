#! /usr/bin/python3

from flask import Flask, jsonify, abort
from mta.mta_info import MTAInfo
import os

app = Flask(__name__)
api_key = os.environ["MTA_API_KEY"]
mta_info = MTAInfo(api_key)

@app.route("/stop/<string:stop_id>")
def stop(stop_id):
    try:
        arrivals = mta_info.get_stop_arrivals(stop_id=stop_id)
        return jsonify(arrivals)
    except KeyError:
        abort(404)
