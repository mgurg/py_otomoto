from flask import Blueprint, render_template, flash
from flask import current_app as app

from .forms import CarForm
from .predict import calulate_price

# Blueprint Configuration
car_bp = Blueprint('car_bp', __name__,
                    template_folder='templates')

@car_bp.route('/report')
def report():
    return render_template('report.html')


@car_bp.route('/car', methods=['GET'])
def car():
    """Homepage."""
    # return "Hello World!"
    return render_template('car.html')

@car_bp.route('/price', methods=['GET', 'POST'])
def form():
    form = CarForm()
    if form.validate_on_submit():
        car_details = {
                        'private_business' : int(1),
                        'year' : int(form.year.data),
                        'mileage' : int(form.mileage.data),
                        'door_count' : int(form.doors.data),
                        'origin_pl' :  int(1),
                        'f_0' : int(0),
                        'f_ac' :  form.air_conditioning.data,
                        'f_alloy-wheels': form.alloy_wheels.data,
                        'f_rear-parking-sensors' : form.rear_parking_sensors.data,
                        'f_steering-whell-comands' : form.steering_whell_comands.data,
                        'f_fog-lights' : form.fog_lights.data,
                        'f_mp3' : form.mp3.data,
                        'f_front-electric-windows' : form.front_electric_windows.data,
                        'f_central-lock' : form.central_lock.data
}

        price = calulate_price(car_details)

        flash('''Wartosc samochodu: {:.2f},
                Klimatyzacja: {},
                Elektryczne szyby przednie: {},
                Centralny zamek: {},
                Alufelgi: {},
                Czujniki parkowania tylne: {},
                MP3: {},
                Światła przeciwmgielne: {},
                Wielofunkcyjna kierownica: {}
                '''
                .format(price,
                        form.air_conditioning.data,
                        form.front_electric_windows.data,
                        form.central_lock.data,
                        form.alloy_wheels.data,
                        form.rear_parking_sensors.data,
                        form.mp3.data,
                        form.fog_lights.data,
                        form.steering_whell_comands.data))

    return render_template('price.html', form=form)