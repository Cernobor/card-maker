from flask import Flask, render_template, send_file, flash
from time import sleep
from card_maker.app.card_maker import create_free_aspect
from card_maker.web.forms import AspektForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1292023cdb7b8e39f924afab' # change to environ => dockerfile

@app.route("/aspekt", methods=["GET","POST"])
def aspekt_create():
    form = AspektForm()

    if form.validate_on_submit():
        name = form.name.data
        effect = form.effect.data
        frame = form.frame.data
        fluff = form.fluff.data
        activation = form.activation.data
        inactivation = form.inactivation.data
        additional_effect = form.additional_effect.data
        aspekt = create_free_aspect(name, effect, frame, fluff, activation, inactivation, additional_effect)
        return send_file(aspekt, mimetype="image/png", as_attachment=True)


    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Toto jste podělali: {err_msg[0]}', category='danger')
    


    return render_template("aspekt.html", form=form)
    
@app.route("/preview", methods=["GET"])
def card_preview():
    img_source = r"/home/jakub-rutrle/code_main/card-maker/card_maker/web/static/default.png"
    return render_template("preview.html", img_source=img_source)