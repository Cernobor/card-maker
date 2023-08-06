from flask import Flask, render_template
from time import sleep

app = Flask(__name__)


@app.route("/aspekt", methods=["GET","POST"])
def vytvor_karticku_aspektu(jmeno_aspektu: str = "aspekt", text_aspektu: str = "foo", fluff: str = "bar"):

    return render_template("aspekt.html")