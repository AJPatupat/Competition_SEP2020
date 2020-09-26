import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def solve(books, days):

    while len(days) > 0 and days[0] < books[0]:
        days.pop(0)

    running = 0
    for i in range(len(books)):
        running += books[i]
        if running > sum(days):
            books = books[:i]
            break

    if len(books) < 2:
        return len(books)

    max = 0
    for i in range(len(books)):
        if books[i] <= days[0]:
            booksCopy = list(books)
            daysCopy = list(days)
            daysCopy[0] -= booksCopy.pop(i)
            result = 1 + solve(booksCopy, daysCopy)
            if result == len(books):
                return result
            if max < result:
                max = result
        else:
            break
    return max


@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateOlympiad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    books = data["books"]
    days = data["days"]
    books.sort()
    days.sort()
    result = {"optimalNumberOfBooks": solve(books, days)}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



