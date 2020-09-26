import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluateIntelligentFarming():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    runId = data.get("runId")
    tests = data.get("list");

    for i in range(len(tests)):
        geneSequence = tests[i]["geneSequence"]

        countA = geneSequence.count("A")
        countC = geneSequence.count("C")
        countG = geneSequence.count("G")
        countT = geneSequence.count("T")
        
        countACGT = min([countA, countC, countG, countT])
        countA  = countA - countACGT
        countC  = countC - countACGT
        countG  = countG - countACGT
        countT  = countT - countACGT        

        tests[i]["geneSequence"] = geneSequence

    result = {"runId" : runId, "list": tests}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



