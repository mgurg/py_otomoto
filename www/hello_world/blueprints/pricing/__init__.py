# -*- coding: utf-8 -*-
from flask import render_template, flash
from flask import Blueprint

from .forms import CarForm
from .predict import calulate_price

pricing_blueprint = Blueprint('pricing_blueprint', __name__)

@pricing_blueprint.route('/pricing', methods=['GET', 'POST'])
def form():
    form = CarForm()
    if form.validate_on_submit():
        feat_dict =	{
            "year" : int(form.year.data),
            "mileage" : int(form.mileage.data),
            "air_conditioning" : form.air_conditioning.data,
            "front_electric_windows" : form.front_electric_windows.data,
            }

        price = calulate_price(feat_dict)

        flash('Wartosc samochodu: {:.2f}, AC: {}'.format(price, form.air_conditioning.data))
    return render_template('price_predict.html', form=form)

