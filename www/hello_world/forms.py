from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Regexp, ValidationError
import re

class LoginForm(FlaskForm):
    year = StringField('Rocznik', validators=[InputRequired(), Regexp("\d{4}", message="Podaj poprawny rok np.: 2009")])
    mileage = StringField('Przebieg', validators=[InputRequired(), Regexp("^[0-9]*$", message="Podaj poprawny przebieg")])
    fuel = SelectField('Rodzaj paliwa:',
                        choices=[('petrol', 'benzyna'), ('diesel', 'diesel'), ('petrol-lpg', 'benzyna+lpg')],
                        default='benzyna')
    air_conditioning = BooleanField('Klimatyzacja')
    front_electric_windows = BooleanField('Elektryczne szyby przednie')
    submit = SubmitField(label="Submit")