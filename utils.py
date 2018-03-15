from urllib.parse import urlencode

import requests
from pymongo import MongoClient

from config import APP_ID, MONGO_URL


def api_url_json(endpoint, zc):
    params = urlencode(dict(zip='{0},us'.format(zc), appid=APP_ID))
    url = 'http://api.openweathermap.org/data/2.5/{0}?{1}'.format(endpoint, params)
    return requests.get(url).json()


def get_db():
    client = MongoClient(MONGO_URL)
    db = client.weatherUpdate
    return db


def push_data_to_db(name, json_data):
    db = get_db()
    collection = getattr(db, name)
    collection.insert(json_data)


def add_field(json_data):
    date_stamp_start = json_data['list'][0]['dt']
    date_stamp_end = json_data['list'][-1]['dt']
    json_data['start_date'] = date_stamp_start
    json_data['end_date'] = date_stamp_end
    return json_data


def open_map_url(map_type, latitude, longitude):
    params = urlencode(dict(basemap='map',
                            cities='true',
                            layer=map_type,
                            lat=latitude,
                            lon=longitude,
                            zoom=10))
    url = 'http://openweathermap.org/weathermap?{0}'.format(params)
    return url
