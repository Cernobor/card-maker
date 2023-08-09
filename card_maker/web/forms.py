from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class AspektForm(FlaskForm):
    jmeno_aspektu = StringField("Jméno aspektu", validators=[DataRequired()])
    text_aspektu = TextAreaField("Text aspektu", validators=[DataRequired()])
    fluff = TextAreaField("Fluff", validators=[DataRequired()])
    submit = SubmitField("Vytvořit kartičku")