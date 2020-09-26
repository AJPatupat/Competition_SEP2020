import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def evaluateRevisitGeometry():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    P = data.get("shapeCoordinates")
    L = data.get("lineCoordinates")
    x = L[0]["x"]
    y = L[0]["y"]
    dx = L[0]["x"] - L[1]["x"]
    dy = L[0]["y"] - L[1]["y"]

    ans = []

    for i in range(len(P)):
        j = i + 1
        if j == len(P):
            j = 0
        numerator = (P[i]["x"] - x) * dy - (P[i]["y"] - y) * dx
        denominator = (P[i]["x"] - P[j]["x"]) * dy - (P[i]["y"] - P[j]["y"]) * dx
        if denominator == 0:
            continue
        t = numerator / denominator
        if t >= 1 or t <= 0:
            continue
        p = { "x": P[i]["x"] + t * (P[j]["x"] - P[i]["x"]), "y": P[i]["y"] + t * (P[j]["y"] - P[i]["y"])}
        ans.append(p)

    result = ans
    logging.info("My result :{}".format(result))
    return json.dumps(result)