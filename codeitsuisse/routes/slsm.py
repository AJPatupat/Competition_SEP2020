import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/slsm', methods=['POST'])
def evaluateSLSM():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    n = data["boardSize"]
    p = data["players"]
    jumps = data["jumps"]

    snakeHigh = []
    snakeLow = []
    ladderHigh = []
    ladderLow = []
    smoke = []
    mirror = []
    steps = list(range(n*n, -n, -n))
    nexts = list(range(0, n+1, 1))

    for j in jumps:
        jList = j.split(':')
        jFirst = int(jList[0])
        jSecond = int(jList[1])
        if jFirst == 0:
            mirror.append(jSecond)
        elif jSecond == 0:
            smoke.append(jFirst)
        elif jFirst < jSecond:
            ladderLow.append(jFirst)
            ladderHigh.append(jSecond)
        else:
            snakeHigh.append(jFirst)
            snakeLow.append(jSecond)

    for i in range(n, 0, -1):

        if i in snakeHigh:
            continue
        elif i in snakeLow:
            steps[snakeHigh[snakeLow.index(i)]] = steps[i]
            nexts[snakeHigh[snakeLow.index(i)]] = i
        elif i in ladderHigh:
            steps[ladderLow[ladderHigh.index(i)]] = steps[i]
            nexts[ladderLow[ladderHigh.index(i)]] = i
        elif i in smoke:
            continue

        s = steps[i] + 1
        for die in range(1, min(7, i)):            
            d = i - die
            if steps[d] > s and (d not in ladderLow) and (d not in snakeHigh):
                steps[d] = s
                nexts[d] = i

    i = 1
    best = []
    bestSub = []
    while i < n:
        logging.info("My path :{}".format(i))
        if i in ladderLow or i in snakeHigh:
            i = nexts[i]
            continue
        bestSub.append(nexts[i] - i)
        if nexts[i] in mirror:
            i = nexts[i]
            continue
        i = nexts[i]
        best.append(list(bestSub))
        bestSub = []
    if len(bestSub) > 0:
        best.append(list(bestSub))

    answer = []
    while len(best) > 1:
        b = best.pop(0)
        for i in range(p):
            answer = answer + b
    b = best.pop(0)
    for i in range(p-1):
        answer = answer + b
        if answer[-1] > 1:
            answer[-1] -= 1
        else:
            answer[-1] += 1
    answer = answer + b

    logging.info("My result :{}".format(answer))
    return json.dumps(answer);



