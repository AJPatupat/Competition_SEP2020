import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

memo = {}

def solve(key, k):

    n = len(key)
    nEven = (n % 2 == 0)
    nHalf = n // 2

    if k == 1 and nEven:
        ans = 0
        for i in range(nHalf):
            if key[i] == "Y" or key[-i-1] == "Y":
                ans += 1
        return ans / nHalf

    if k == 1 and not nEven:
        ans = 0
        for i in range(nHalf):
            if key[i] == "Y" or key[-i-1] == "Y":
                ans += 1
        ans *= 2
        if key[nHalf] == "Y":
            ans += 1
        return ans / n

    new_key = key[1:]
    if new_key not in memo[k-1]:
        memo[k-1][new_key] = solve(new_key, k-1)
    for i in range(len(new_key)):
        if new_key[i] == key[i]:
            continue
        new_list = list(new_key)
        new_list[i] = key[i]
        new_key = ''.join(new_list)
        if new_key not in memo[k-1]:
            memo[k-1][new_key] = solve(new_key, k-1)

    new_key_1 = key[1:]
    new_key_2 = key[:-1]

    if nEven:
        ans = 0
        for i in range(nHalf):
            val_1 = memo[k-1][new_key_1]
            val_2 = memo[k-1][new_key_2]
            if key[i] == "Y":
                val_1 += 1
            if key[n-1-i] == "Y":
                val_2 += 1
            ans += max(val_1, val_2)
            if i == nHalf - 1:
                break
            list_1 = list(new_key_1)
            list_1[i] = key[i]
            new_key_1 = ''.join(list_1)
            list_2 = list(new_key_2)
            list_2[n-2-i] = key[n-1-i]
            new_key_2 = ''.join(list_2)
        return ans / nHalf

    if not nEven:
        ans = 0
        for i in range(nHalf):
            val_1 = memo[k-1][new_key_1]
            val_2 = memo[k-1][new_key_2]
            if key[i] == "Y":
                val_1 += 1
            if key[n-1-i] == "Y":
                val_2 += 1
            ans += max(val_1, val_2)
            list_1 = list(new_key_1)
            list_1[i] = key[i]
            new_key_1 = ''.join(list_1)
            list_2 = list(new_key_2)
            list_2[n-2-i] = key[n-1-i]
            new_key_2 = ''.join(list_2)
        ans *= 2
        val_1 = memo[k-1][new_key_1]
        if key[nHalf] == "Y":
            val_1 += 1
        ans += val_1
        return ans / n


@app.route('/yin-yang', methods=['POST'])
def evaluateYinYang():
    data = request.get_json();
    #logging.info("data sent for evaluation {}".format(data))

    key = data["elements"]
    k = data["number_of_operations"]
    if len(key) == k:
        result = key.count("Y")
    else:
        memo = []
        for i in range(k):
            memo.append({})
        result = solve(key, k)
        memo = []    

    response = app.response_class(
        response=json.dumps({"result" : result}),
        status=200,
        mimetype='application/json'
    )

    #logging.info("My result :{}".format(result))
    return response;



