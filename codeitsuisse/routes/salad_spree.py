import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSaladSpree():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    n = data.get("number_of_salads")
    S = data.get("salad_prices_street_map")

    minExists = False
    min = 0

    for s in S:
        runningSum = 0
        runningCount = 0
        for i in range(len(s)):
            if s[i] == "X":
                runningSum = 0
                runningCount = 0
            elif runningCount == n:
                runningSum = runningSum + int(s[i]) - int(s[i-n])
            else:
                runningSum = runningSum + int(s[i])
                runningCount = runningCount + 1
            if runningCount == n:
                if not minExists or min > runningSum:
                    minExists = True
                    min = runningSum

    result = {"result": min}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



