@@ -1,147 +0,0 @@
from flask import Flask, render_template, redirect, session, url_for, flash, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Regexp, ValidationError

import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
import bokeh_catplot
import yaml

from functions import get_data, predict_car_price

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

app = Flask(__name__)
app.config['SECRET_KEY'] = cfg['flask']['wtf_password']

#otomoto_blueprint = Blueprint('otomoto_blueprint', __name__)

df = get_data()

class LoginForm(FlaskForm):
    year = StringField('Rocznik', validators=[InputRequired(), Regexp("\d{4}", message="Podaj poprawny rok np.: 2009")])
    mileage = StringField('Przebieg', validators=[InputRequired(), Regexp("^[0-9]*$", message="Podaj poprawny przebieg")])
    fuel = SelectField('Rodzaj paliwa:',
                        choices=[('petrol', 'benzyna'), ('diesel', 'diesel'), ('petrol-lpg', 'benzyna+lpg')],
                        default='benzyna')
    air_conditioning = BooleanField('Klimatyzacja')
    front_electric_windows = BooleanField('Elektryczne szyby przednie')
    submit = SubmitField(label="Submit")

    # https://www.youtube.com/watch?v=xRZwU9lqUbs
    # https://github.com/soumilshah1995/Flask-Captcha-Python

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/otomoto")
def otomoto():
    return render_template("otomoto.html")

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        year = int(form.year.data)
        mileage = int(form.mileage.data)

        feat_dict =	{
            "air_conditioning": form.air_conditioning.data,
            "front_electric_windows": form.front_electric_windows.data,
            }

        features = [form.air_conditioning.data, form.front_electric_windows.data]

        price = predict_car_price(year, mileage)
        flash('Wartość samochodu: {}, AC: {}'.format(price, form.air_conditioning.data))
        #return '<h1>Cena powinna wynosić: {}<h1>'.format(price)
        # return '<h1>Year: {}. Mileage {}. Fuel {}<h1>'.format(form.year.data, form.mileage.data, form.fuel.data)
        #return redirect(url_for('bokeh'))
    return render_template('form.html', form=form)

@app.route('/bokeh')
def bokeh():

    p = bokeh_catplot.histogram(data=df['price'],cats=None,val='price', bins=20)

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(plot_width=600, plot_height=600)
    fig.vbar(
        x=[1, 2, 3, 4],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'bokeh.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        show_bokeh=True,
    )
    return html.encode('utf-8')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('profile'))

    error = None
    class ServerError(Exception):pass

    # if request.method == 'POST':
    #     if request.form["action"] == "login":
    #         try:
    #             conn = mysql.connect()
    #             cur = conn.cursor()
    #             username_form  = request.form['username']
    #             cur.execute("SELECT COUNT(1) FROM users WHERE login = '" + username_form +"'")

    #             if not cur.fetchone()[0]:
    #                 raise ServerError('Błędna nazwa użytkownika')

    #             password_form  = request.form['password']
    #             cur.execute("SELECT password FROM users WHERE login = '" + username_form +"'")

    #             for row in cur.fetchall():
    #                 if md5(password_form.encode('utf-8')).hexdigest() == row[0]:
    #                     session['username'] = request.form['username']
    #                     return redirect(url_for('db_posts_blueprint.database_posts'))

    #             raise ServerError('Błędne hasło')

    #         except ServerError as e:
    #             error = str(e)

    return render_template('login.html', error=error)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0' )

# https://www.youtube.com/watch?v=jR2aFKuaOBs&list=PLXmMXHVSvS-C_T5JWEDWIc9yEM3Hj52-1&index=6