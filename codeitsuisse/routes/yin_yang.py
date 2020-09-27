import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

memo = {}

def solve(key, k):

    if k == 1:
        ans = 0
        for i in range(len(key)):
            if key[i] == "Y" or key[-i-1] == "Y":
                ans += 1
        return ans / len(key)

    if k-1 not in memo:
        memo[k-1] = {}

    for i in range(len(key)):        
        new_key = ''.join([key[j] for j in range(len(key)) if j != i])
        if new_key not in memo[k-1]:
            memo[k-1][new_key] = solve(new_key, k-1)

    s = 0
    for i in range(len(key)):
        new_key_1 = ''.join([key[j] for j in range(len(key)) if j != i])
        new_key_2 = ''.join([key[j] for j in range(len(key)) if j != len(key)-1-i])
        val_1 = memo[k-1][new_key_1]
        val_2 = memo[k-1][new_key_2]
        if key[i] == "Y":
            val_1 += 1
        if key[len(key)-1-i] == "Y":
            val_2 += 1
        s += max(val_1, val_2)

    return s / len(key)


@app.route('/yin-yang', methods=['POST'])
def evaluateYinYang():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    key = data["elements"]
    k = data["number_of_operations"]
    result = solve(key, k)
    memo = {}

    response = app.response_class(
        response=json.dumps({"result" : result}),
        status=200,
        mimetype='application/json'
    )

    logging.info("My result :{}".format(result))
    return response;



