import joblib
import pandas as pd
import xgboost

def calulate_price(car_feats):
    feats = ['private_business', 'year', 'mileage', 'door_count', 'origin_pl', 'f_0', 'f_central-lock',
    'f_alloy-wheels', 'f_ac', 'f_rear-parking-sensors', 'f_mp3', 'f_front-electric-windows', 'f_fog-lights', 'f_steering-whell-comands']

    car_info = pd.DataFrame(columns = feats)
    car_info = car_info.append(car_feats , ignore_index=True)

    loaded_model = joblib.load('./hello_world/bp_car/yaris_200530.pkl')
    result = loaded_model.predict(car_info.values)

    return result[0]