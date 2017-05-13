from flask import Flask
import requests
app = Flask(__name__)

API_KEY = 'FMnkufGpV3xvG9R2jQKjeVIi85nW5EIOP5sB5c2N'
PROJECT_ID = 'hackath2on-562dd'
BDDD_URL = 'https://hackath2on-562dd.firebaseio.com/'

# Todas las requests tienen que tener este formato
# 'https://hackath2on-562dd.firebaseio.com/entity.json?access_token=FMnkufGpV3xvG9R2jQKjeVIi85nW5EIOP5sB5c2N'


@app.route("/")
def hello():
    return "Hello World!"

def sampleGET():
    r = requests.get(BDDD_URL + "users/SAMPLEID")
    #tratar objecto request "r"


def main():
    app.run()

if __name__ == '__main__':
    main()