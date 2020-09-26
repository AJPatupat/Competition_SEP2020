import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def checkDiff(str1, str2):
    diffs = []
    for i in range(len(str1)):
        if not str1[i] == str2[i]:
            diffs.append(i)
            if len(diffs) > 2:
                return 0
    if len(diffs) == 2 and diffs[0] % 4 == 0 and diffs[1] % 4 == 0:
        return 2    
    return 1

def recordNamePath(namePath, answer):
    ans = ""
    for n in namePath:
        ans += n
    answer.append(ans)

def check(namePath, genomeLast, origin, cluster, answer):

    res = checkDiff(genomeLast, origin["genome"])
    if res == 2:
        namePath.append("* -> ")
        namePath.append(origin["name"])
        recordNamePath(namePath, answer)
        namePath = namePath[:-2]
    elif res == 1:
        namePath.append(" -> ")
        namePath.append(origin["name"])
        recordNamePath(namePath, answer)
        namePath = namePath[:-2]

    for node in cluster:
        if node["name"] in namePath:
            continue
        res = checkDiff(genomeLast, node["genome"])
        if res == 2:
            namePath.append("* -> ")
            namePath.append(node["name"])
            if origin["genome"] == node["genome"]:
                recordNamePath(namePath, answer)
            else:
                check(namePath, origin["genome"], origin, cluster, answer)
            namePath = namePath[:-2]
        elif res == 1:
            namePath.append(" -> ")
            namePath.append(node["name"])
            if origin["genome"] == node["genome"]:
                recordNamePath(namePath, answer)
            else:
                check(namePath, origin["genome"], origin, cluster, answer)
            namePath = namePath[:-2]


@app.route('/contact_trace', methods=['POST'])
def evaluateContractTracing():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    infected = data["infected"]
    origin = data["origin"]
    cluster = data["cluster"]

    answer = []
    namePath = [infected["name"]]

    check(namePath, infected["genome"], origin, cluster, answer)

    if len(answer) == 0:
        answer.append("")

    logging.info("My result :{}".format(answer))
    return json.dumps(answer);



