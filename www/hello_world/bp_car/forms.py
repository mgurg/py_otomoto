from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Regexp, ValidationError
import re

class CarForm(FlaskForm):
    year = StringField('Rocznik', validators=[InputRequired(), Regexp("\d{4}", message="Podaj poprawny rok np.: 2009")])
    mileage = StringField('Przebieg', validators=[InputRequired(), Regexp("^[0-9]*$", message="Podaj poprawny przebieg")])
    fuel = SelectField('Rodzaj paliwa:',
                        choices=[('petrol', 'benzyna'), ('diesel', 'diesel'), ('petrol-lpg', 'benzyna+lpg')],
                        default='benzyna')
    doors = SelectField('Liczba drzwi:',
                        choices=[('5', '5'), ('3', '3')],
                        default='5')

    front_electric_windows = BooleanField('Elektryczne szyby przednie')
    central_lock = BooleanField('Centralny zamek')
    alloy_wheels = BooleanField('Alufelgi')
    air_conditioning = BooleanField('Klimatyzacja')
    rear_parking_sensors = BooleanField('Czujniki parkowania tylne')
    mp3 = BooleanField('MP3')
    front_electric_windows = BooleanField('Elektryczne szyby przednie')
    fog_lights = BooleanField('Światła przeciwmgielne')
    steering_whell_comands = BooleanField('Wielofunkcyjna kierownica')
    submit = SubmitField(label="Wylicz wartość")