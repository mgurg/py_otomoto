import sqlite3
import pandas as pd

def get_data():
    sql_query ="""
SELECT
    all_offers.offer_id,otomoto_all.s_date, otomoto_all.e_date, all_offers.private_business, all_offers.region,
    all_offers.city, all_offers.model, all_offers.year, all_offers.mileage, all_offers.engine_capacity, all_offers.vin,
    all_offers.fuel_type, all_offers.engine_power, all_offers.gearbox, all_offers.transmission, all_offers.door_count,
    all_offers.nr_seats, all_offers.color, all_offers.features,otomoto_all.price, all_offers.price_raw, all_offers.currency,
    all_offers.country_origin, all_offers.registration
FROM
    otomoto_all, all_offers
WHERE
    otomoto_all.uid = all_offers.uid;
"""

    conn = sqlite3.connect("pythonsqlite.db")
    data = pd.read_sql_query(sql_query, conn)
    return data

def predict_price(year, mileage):
    price = mileage + year
    return price