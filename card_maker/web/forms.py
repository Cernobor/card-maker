from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, FieldList, TextAreaField, RadioField


class AspektForm(FlaskForm):
    """
    Form for creating aspekt
    """
    name = StringField('Jméno aspektu', validators=[DataRequired()])
    effect = TextAreaField('Efekt aspektu', validators=[DataRequired()])
    frame = RadioField('Velikost kartičky', choices=[('normal', 'normální'), ('large', 'velká')], default="normal")
    fluff = TextAreaField('Fluff')
    activation = TextAreaField('Aktivace')
    inactivation = TextAreaField('Inactivation')
    additional_effect = FieldList(StringField(''), min_entries=4)
    submit = SubmitField('Vytvořit & stáhnout')

