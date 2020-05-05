import joblib
import pandas as pd
import xgboost

def calulate_price(car_feats):
    feats = ['year', 'mileage', 'engine_capacity', 'engine_power', 'door_count', 'nr_seats', 'duration', 'price_chng',
    'f_front-side-airbags', 'f_velour-interior', 'f_front-electric-windows', 'f_electronic-rearview-mirrors',
    'f_electric-exterior-mirror', 'f_electric-adjustable-seats', 'f_electronic-immobiliser', 'f_alloy-wheels',
    'f_sd-socket', 'f_usb-socket', 'f_dual-air-conditioning', 'f_rear-electric-windows', 'f_rear-passenger-airbags',
    'f_esp', 'f_asr', 'f_gps', 'f_driver-knee-airbag', 'f_cd-changer', 'f_front-heated-seats', 'f_head-display',
    'f_air-conditioning', 'f_tinted-windows', 'f_shift-paddles', 'f_towing-hook', 'f_front-airbags', 'f_daytime-lights',
    'f_onboard-computer', 'f_automatic-air-conditioning', 'f_cd', 'f_heated-rearview-mirrors', 'f_side-window-airbags',
    'f_front-passenger-airbags', 'f_alarm', 'f_steering-whell-comands', 'f_assisted-steering', 'f_automatic-wipers',
    'f_electric-interior-mirror', 'f_fog-lights', 'f_park-assist', 'f_abs', 'f_roof-bars', 'f_aux-in',
    'f_automatic-lights', 'f_original-radio', 'f_bluetooth', 'f_central-lock', 'f_0', 'f_isofix',
    'f_rear-parking-sensors', 'f_leds', 'f_cruise-control', 'f_system-start-stop']

    car_info = pd.DataFrame(columns = feats)
    car_info = car_info.append(car_feats , ignore_index=True)

    loaded_model = joblib.load('./hello_world/blueprints/pricing/yaris_200405.pkl')
    result = loaded_model.predict(car_info.values)

    return result[0]