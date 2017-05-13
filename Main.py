from flask import Flask
from flask import request
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
    json = {
        "email": email,
        "lat":lat,
        "lon":lon
    }
    r = requests.post(BDDD_URL + "users/" + identifier + ".json?auth=" + API_KEY, json=json, headers=HEADERS)
    return r.json()


@app.route("/users/:ID/complains")
def register_user2():
    # sacar ID
    # sacar email
    # sacar lat, lon
    # enviarlos en POST
    r = requests.post(BDDD_URL + "users/" + ID)


@app.route("/users/:ID/complains/:complainID/answer")
def register_user3():
    # sacar ID
    # sacar email
    # sacar lat, lon
    # enviarlos en POST
    r = requests.post(BDDD_URL + "users/" + ID)


def main():
    app.run()


if __name__ == '__main__':
    main()
