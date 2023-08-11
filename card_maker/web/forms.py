from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField, RadioField


class AspektForm(FlaskForm):
    """
    Form for creating aspekt
    """
    name = StringField('Jméno aspektu', validators=[DataRequired()])
    effect = TextAreaField('Efekt aspektu', validators=[DataRequired()])
    frame = RadioField('Velikost kartičky', choices=[('normal', 'normální'), ('large', 'velká')], default="normal")
    fluff = StringField('Fluff')
    activation = StringField('Aktivace')
    inactivation = StringField('Inactivation')
    additional_effect = StringField('Additional Effect')
    submit = SubmitField('Submit')

