import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def solve(books, days):

    min = len(books)
    for i in range(len(books)):
        booksCopy = list(books)
        daysCopy = list(days)
        while len(daysCopy) > 0 and daysCopy[0] < booksCopy[i]:
            daysCopy.pop(0)
        if len(daysCopy) == 0:
            continue
        daysCopy[0] -= booksCopy.pop(i)
        result = solve(booksCopy, daysCopy)
        if result == 0:
            return 0
        if min > result:
            min = result
    return min

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateOlympiad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    books = data["books"]
    days = data["days"]
    result = len(books) - solve(books, days)
    result = {"optimalNumberOfBooks": result}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



