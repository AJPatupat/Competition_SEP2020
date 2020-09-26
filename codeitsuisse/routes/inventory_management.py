import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def lev(a,b):

    arr = []
    for i in range(0, len(a)+1):
        arr.append([i])
    for j in range(1, len(b)+1):
        arr[0].append(j)

    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1].lower() == b[j-1].lower():
                arr[i].append( min( [ arr[i-1][j]+1, arr[i][j-1]+1, arr[i-1][j-1] ] ) )
            else:
                arr[i].append( min( [ arr[i-1][j]+1, arr[i][j-1]+1, arr[i-1][j-1]+1 ] ) )

    ans = ""
    i = len(a)
    j = len(b)
    while i > 0 and j > 0:
        if arr[i][j] == arr[i-1][j]+1:
            ans = "-" + a[i-1] + ans
            i -= 1
        elif arr[i][j] == arr[i][j-1]+1:
            ans = "+" + b[j-1] + ans
            j -= 1
        elif a[i-1] == b[j-1]:
            ans = a[i-1] + ans
            i -= 1
            j -= 1
        else:
            ans = b[j-1].lower() + ans
            i -= 1
            j -= 1
    if j == 0:
        while not i == 0:
            ans = "-" + a[i-1] + ans
            i -= 1
    if i == 0:
        while not j == 0:
            ans = "+" + b[j-1] + ans
            j -= 1

    return arr[len(a)][len(b)], ans
            

@app.route('/inventory-management', methods=['POST'])
def evaluateInventoryManagement():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for d in data:

        base = d["searchItemName"]
        choices = d["items"]

        choicesArr = []
        for choice in choices:
            key, word = lev(base, choice)
            choicesArr.append({"key" : key, "word" : word, "orig": choice})

        answer = []
        while len(choicesArr) > 0 and len(answer) < 10:
            minIndex = 0
            for i in range(len(choicesArr)):
                if choicesArr[minIndex]["key"] > choicesArr[i]["key"]:
                    minIndex = i
                elif choicesArr[minIndex]["key"] == choicesArr[i]["key"] and choicesArr[minIndex]["orig"] > choicesArr[i]["orig"]:
                    minIndex = i
            answer.append(choicesArr.pop(minIndex)["word"])

        result.append({"searchItemName": base, "searchResult": answer})

    logging.info("My result :{}".format(result))
    return json.dumps(result);



