#GOOGLEPLACES API = AIzaSyCiT_v1UiAVzG3Shd4c5RxXxFncu5_d9YU
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
