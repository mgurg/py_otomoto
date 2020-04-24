from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import InputRequired

import pandas as pd
from functions import get_data

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
import bokeh_catplot
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

#from bokeh.util.string import encode_utf8

app = Flask(__name__)
app.config['SECRET_KEY'] = cfg['flask']['wtf_password']
df = get_data()


class LoginForm(FlaskForm):
    year = StringField('Rocznik', validators=[InputRequired()])
    mileage = StringField('mileage',validators=[InputRequired()])
    fuel = SelectField('fuel',
                        choices=[('petrol', 'benzyna'), ('diesel', 'diesel'), ('petrol+lpg', 'beznyna+lpg')],
                        default='benzyna')
    air_conditioning = BooleanField('Klimatyzacja')
    front_electric_windows = BooleanField('Elektryczne szyby przednie')



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
        return '<h1>Year: {}. Mileage {}. Fuel {}'.format(form.year.data, form.mileage.data, form.fuel.data)
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

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0' )

# https://www.youtube.com/watch?v=jR2aFKuaOBs&list=PLXmMXHVSvS-C_T5JWEDWIc9yEM3Hj52-1&index=6
