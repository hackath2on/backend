from flask import Flask
from flask import request
from flask import Response
import datetime
import uuid

import requests

app = Flask(__name__)

API_KEY = 'FMnkufGpV3xvG9R2jQKjeVIi85nW5EIOP5sB5c2N'
PROJECT_ID = 'hackath2on-562dd'
BDDD_URL = 'https://hackath2on-562dd.firebaseio.com/'
HEADERS = {'Authorization': 'Bearer ' + API_KEY}
ELASTIC_SEARCH_BASE = "http://localhost:9200"


# Todas las requests tienen que tener este formato
# 'https://hackath2on-562dd.firebaseio.com/entity.json?access_token=FMnkufGpV3xvG9R2jQKjeVIi85nW5EIOP5sB5c2N'


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sampleGET")
def sample_get():
    r = requests.get(BDDD_URL + "users/SAMPLEID")
    # tratar objecto request "r"


def post_user_es(id, params):
    r = requests.post(ELASTIC_SEARCH_BASE + "/users/user/" + id, json=params)
    print(r.text)


def post_complaint_es(id, params):
    r = requests.post(ELASTIC_SEARCH_BASE + "/complaints/complaint/" + id, json=params)
    print(r.text)


def post_answer_es(id, params):
    r = requests.post(ELASTIC_SEARCH_BASE + "/answers/answer/" + id, json=params)
    print(r.text)


@app.route("/users/<id>", methods=['POST'])
def register_user(id=None):
    identifier = id
    email = request.args.get('email')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    fcmToken = request.args.get('fcm_token')
    json = {
        "email": email,
        "location": {
            "lat": request.args.get("lat"),
            "lon": request.args.get("lon")
        },
        "fcm_token": fcmToken,
        "created_at": str(datetime.datetime.now().isoformat())
    }
    r = requests.put(BDDD_URL + "users/" + identifier + ".json?auth=" + API_KEY, json=json, headers=HEADERS)
    response = Response(r.text)
    response.headers['Content-Type'] = 'application/json'
    post_user_es(id, json)
    return response


@app.route("/users/<id>/complains", methods=['POST'])
def create_complain(id=None):
    identifier = id
    image_url = ""
    if "image_url" in request.args:
        image_url = request.args.get('image_url')
    title = request.args.get('title')
    location = {}
    location['lat'] = request.args.get('lat')
    location['lon'] = request.args.get('lon')

    json = {
        "image_url": image_url,
        "location": location,
        "title": title,
        "user_id": identifier,
        "created_at": str(datetime.datetime.now().isoformat())
    }
    r = requests.post(BDDD_URL + "/complains.json?auth=" + API_KEY, json=json, headers=HEADERS)
    complain_id = r.json()['name']
    post_complaint_es(complain_id, json)
    response = Response(r.text)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route("/users/<user_id>/complains/<complain_id>/answers", methods=['POST'])
def answer(user_id=None, complain_id=None):
    uuid_value = str(uuid.uuid4())
    url = BDDD_URL + "complains/" + complain_id + "/answers/" + uuid_value + ".json?auth=" + API_KEY
    json = {
        "answer": request.args.get('answer'),
        "location": {
            "lat": request.args.get("lat"),
            "lon": request.args.get("lon")
        },
        "userID": user_id,
        "created_at": str(datetime.datetime.now().isoformat())
    }
    r = requests.put(url=url, json=json, headers=HEADERS)
    response = Response(r.text)
    response.headers['Content-Type'] = 'application/json'
    post_answer_es(uuid_value, json)
    return response


def main():
    app.run(port=4000)


if __name__ == '__main__':
    main()
