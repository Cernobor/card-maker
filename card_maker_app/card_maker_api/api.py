from flask import Flask
from time import sleep

app = Flask(__name__)


@app.route("/aspekt", methods=["GET"])
def vytvor_karticku_aspektu(jmeno_aspektu: str = "aspekt", text_aspektu: str = "foo", fluff: str = "bar"):
    sleep(10)
    return {"jmeno_aspektu": jmeno_aspektu, "text_aspektu": text_aspektu, "fluff": fluff}