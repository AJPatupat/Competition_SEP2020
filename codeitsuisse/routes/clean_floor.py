import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluateCleanFloor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    tests = data.get("tests")
    answers = {}

    for title, test in tests.items():
        floor = test["floor"]

        max = len(floor) - 1
        while max >= 0 and floor[max] == 0:
            max = max - 1

        moves = 0
        for i in range(len(floor)):

            if floor[max] == 0:
                break

            moves = moves + 2 * floor[i]
            if floor[i+1] > floor[i]:
                floor[i+1] = floor[i+1] - floor[i]
            else:
                floor[i+1] = (floor[i] - floor[i+1]) % 2

            if floor[max] == 0:
                break

            moves = moves + 1
            if floor[i+1] > 0:
                floor[i+1] = floor[i+1] - 1
            else:
                floor[i+1] = 1            

        answers[title] = moves

    result = {"answers" : answers}
    logging.info("My result :{}".format(result))
    return json.dumps(result)