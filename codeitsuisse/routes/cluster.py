import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def check(arr, i, j):

    if i < 0 or i >= len(arr) or j < 0 or j >= len(arr[0]):
        return

    if arr[i][j] == "*":
        return

    arr[i][j] = "*"

    for i1 in [i-1,i,i+1]:
        for j1 in [j-1,j,j+1]:
            check(arr, i1, j1)

    return

@app.route('/cluster', methods=['POST'])
def evaluateCluster():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    clusters = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "1":
                clusters = clusters + 1
                check(data, i, j)

    result = {"answers" : clusters}
    logging.info("My result :{}".format(result))
    return json.dumps(result)