from flask import Flask, render_template, send_file, flash, url_for, after_this_request
from time import sleep
from card_maker.app.card_maker import create_free_aspect
from card_maker.web.forms import AspektForm
import shutil
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '1292023cdb7b8e39f924afab' # change to environ => dockerfile

@app.route("/")
def test_base():
    return render_template("base.html")

@app.route("/aspekt", methods=["GET","POST"])
def aspekt_create():
    form = AspektForm()

    img_basename = "default.png"
    
    

    if form.validate_on_submit():
        name = form.name.data
        effect = form.effect.data
        frame = form.frame.data
        fluff = form.fluff.data
        activation = form.activation.data
        inactivation = form.inactivation.data
        additional_effect = form.additional_effect.data
        additional_effect = list(filter(None, additional_effect))

        aspekt_path = create_free_aspect(name, effect, frame, fluff, activation, inactivation, additional_effect)

        new_path = os.path.join(os.path.dirname(__file__),"static","created_cards", os.path.basename(aspekt_path))
        shutil.move(aspekt_path, new_path)

        img_basename = os.path.basename(aspekt_path)

        @after_this_request
        def delete_file(response):
            try:
                os.remove(new_path)
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response

        return send_file(new_path, mimetype="image/png", as_attachment=True)


    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Vyskytl se problém: {err_msg[0]}', category='danger', )
    

    
    return render_template("aspekt.html", form=form, img_source=img_basename)
    
@app.route("/preview", methods=["GET"])
def card_preview():
    img_source = r"/home/jakub-rutrle/code_main/card-maker/card_maker/web/static/default.png"
    return render_template("preview.html", img_source=img_source)