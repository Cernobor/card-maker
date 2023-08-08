from flask import Flask, render_template, send_file
from time import sleep

app = Flask(__name__)


@app.route("/aspekt", methods=["GET","POST"])
def vytvor_karticku_aspektu(jmeno_aspektu: str = "aspekt", text_aspektu: str = "foo", fluff: str = "bar"):

    return send_file(r"/home/jakub/Desktop/code_main/card-maker-api/card_maker/web/kapy.png", mimetype="image/png", as_attachment=True)