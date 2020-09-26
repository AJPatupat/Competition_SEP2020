import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluateIntelligentFarming():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    for i in range(len(data["list"])):
        geneSequence = data["list"][i]["geneSequence"]

        countA = geneSequence.count("A")
        countC = geneSequence.count("C")
        countG = geneSequence.count("G")
        countT = geneSequence.count("T")
        
        countACGT = min([countA, countC, countG, countT])
        countA -= countACGT
        countC -= countACGT
        countG -= countACGT
        countT -= countACGT

        if countACGT > 0 and countC % 2 == 1:
            countACGT = countACGT - 1
            countA += 1
            countC += 1
            countG += 1
            countT += 1
        countCC = countC // 2
        countC = countC % 2

        ans = ""

        while countG > 0:
            if countA >= 2:
                ans += "AAG"
                countA -= 2
            elif countA == 1:
                ans += "AG"
                countA -= 1
            else:
                ans += "G"
            countG -= 1

        while countT > 0:
            if countA >= 2:
                ans += "AAT"
                countA -= 2
            elif countA == 1:
                ans += "AT"
                countA -= 1
            else:
                ans += "T"
            countT -= 1

        while countC > 0:
            if countA >= 2:
                ans += "AAC"
                countA -= 2
            elif countA == 1:
                ans += "AC"
                countA -= 1
            else:
                ans += "C"
            countC -= 1

        while countCC > 0:
            if countA >= 2:
                ans += "AACC"
                countA -= 2
            elif countA == 1:
                ans += "ACC"
                countA -= 1
            else:
                ans += "CC"
            countCC -= 1

        while countACGT > 0:
            if countA >= 1:
                ans += "AACGT"
                countA -= 1
            else:
                ans += "ACGT"
            countACGT -= 1

        while countA > 0:
            ans += "A"
            countA -= 1       

        data["list"][i]["geneSequence"] = ans

    logging.info("My result :{}".format(data))

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response



