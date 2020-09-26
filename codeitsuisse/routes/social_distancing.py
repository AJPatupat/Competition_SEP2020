import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluateSocialDistancing():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    tests = data["tests"];
    answers = {}

    for key, info in tests.items():
        answers[key] = ncr(info["seats"] + info["spaces"] - info["spaces"] * info["people"], info["people"])

    result = {"answers" : answers}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



