from flask import Flask
from flask import request
from flask import Response
import uuid

import requests

app = Flask(__name__)

API_KEY = 'FMnkufGpV3xvG9R2jQKjeVIi85nW5EIOP5sB5c2N'
PROJECT_ID = 'hackath2on-562dd'
BDDD_URL = 'https://hackath2on-562dd.firebaseio.com/'
HEADERS = {'Authorization': 'Bearer ' + API_KEY}


# Todas las requests tienen que tener este formato
# 'https://hackath2on-562dd.firebaseio.com/entity.json?access_token=FMnkufGpV3xvG9R2jQKjeVIi85nW5EIOP5sB5c2N'


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sampleGET")
def sample_get():
    r = requests.get(BDDD_URL + "users/SAMPLEID")
    # tratar objecto request "r"


@app.route("/users/<id>", methods=['POST'])
def register_user(id=None):
    identifier = id
    email = request.args.get('email')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    fcmToken = request.args.get('fcm_token')
    json = {
        "email": email,
        "lat": lat,
        "lon": lon,
        "fcm_token": fcmToken
    }
    r = requests.put(BDDD_URL + "users/" + identifier + ".json?auth=" + API_KEY, json=json, headers=HEADERS)
    response = Response(r.text)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route("/users/:ID/complains")
def register_user2():
    # sacar ID
    # sacar email
    # sacar lat, lon
    # enviarlos en POST
    pass


@app.route("/users/<user_id>/complains/<complain_id>/answer", methods=['POST'])
def answer(user_id=None, complain_id=None):
    url = BDDD_URL + "complaints/" + complain_id + "/answers/" + str(uuid.uuid4()) + ".json?auth=" + API_KEY
    json = {
        "answer", request.args.get('answer'),
        "lat", request.args.get("lat"),
        "lon", request.args.get("lon"),
        "userID", user_id
    }
    r = requests.put(url=url, json=json, headers=HEADERS)


def main():
    app.run()


if __name__ == '__main__':
    main()
