from flask import render_template, flash
from flask import Blueprint

from .forms import CarForm

pricing_blueprint = Blueprint('pricing_blueprint', __name__)

@pricing_blueprint.route('/pricing', methods=['GET', 'POST'])
def form():
    form = CarForm()
    if form.validate_on_submit():
        year = int(form.year.data)
        mileage = int(form.mileage.data)

        feat_dict =	{
            "air_conditioning": form.air_conditioning.data,
            "front_electric_windows": form.front_electric_windows.data,
            }

        features = [form.air_conditioning.data, form.front_electric_windows.data]
        price = year + mileage

        flash('Wartość samochodu: {}, AC: {}'.format(price, form.air_conditioning.data))
    return render_template('price_predict.html', form=form)