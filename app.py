from flask import Flask, json
from flask import request
from flask import json
from flask import make_response
import requests as req

app = Flask(__name__)

BASE_URL = "http://marketdata.websol.barchart.com/"
KEY = "b1a585d027c8d89fa27ccd3628609739"
GET_QUOTE = "getQuote.json"
SYMBOLS = "symbols"


@app.route("/")
def hello():
    return 'Hello, world!'


@app.route("/webhook", methods=['POST'])
def handle():
    speech = ""
    body = request.json
    action = body['result']['action']

    if action == 'SEARCH':
        params = body['result']['parameters']
        qs = []
        for key in params:
            if 'Param' in key:
                qs.append(params[key])
        symbols = ''
        symbol_first = True
        for key in params:

            if 'Symbol' in key:
                if symbol_first:
                    symbol_first = False
                    symbols = symbols + params[key]
                else:
                    symbols = symbols + ',' + params[key]

        resp = req.get(BASE_URL + GET_QUOTE, params={'key': KEY, 'symbols': symbols})
        print(resp.text)
        json_response = resp.json()

        for unit_resp in json_response['results']:
            speech = speech + " For {} ".format(unit_resp['name'])
            qs = list(filter((lambda x: x != ""), qs))
            if len(qs) == 0:
                speech = 'What do you want to know about {}'.format(unit_resp['name'])
            else:
                for qs_elem in qs:
                    qs_elem_text = qs_elem
                    if qs_elem == 'lastPrice':
                        qs_elem_text = "last price"
                    if qs_elem == 'netChange':
                        qs_elem_text = "net change"
                    if qs_elem is not None and qs_elem != "":
                        speech = speech + " the {} is {}".format(qs_elem_text, unit_resp[qs_elem])

    data = {
        "speech": speech,
        "displayText": speech,
    }
    js = json.dumps(data)
    r = make_response(js)
    r.headers['Content-Type'] = 'application/json'
    return r


# Request a la API de STOCK
# r = re.get(BASE_URL + GET_QUOTE, params={'key': KEY, 'symbols': symbol})


if __name__ == '__main__':
    app.run(port=4000)
