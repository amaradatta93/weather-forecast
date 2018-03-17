from urllib.parse import urlencode

import requests

from config import APP_ID, DB


def api_url_json(endpoint, zc):
    """
    Fetches the data from the given openWeatherMap endpoint with the zip
    :param endpoint: The openWeatherMap API endpoint (ex: forecast, weather etc)
    :param zc: zip_code
    :return: JSON response
    """
    params = urlencode(dict(zip='{0},us'.format(zc), appid=APP_ID))
    url = 'http://api.openweathermap.org/data/2.5/{0}?{1}'.format(endpoint, params)
    return requests.get(url).json()


def get_db():
    """
    :return: pymongo client for weatherUpdate collection
    """
    return DB.weatherUpdate


def push_data_to_db(name, json_data):
    """
    Persists data in the database
    :param name: The name of the collection
    :param json_data: dictionary
    """
    collection = getattr(get_db(), name)
    collection.insert(json_data)


def add_field(json_data):
    """
    Add the start date and end data to Query the retrieve the required time frame data
    :param json_data: Dictionary to which it is added
    :return: dictionary with start and end date
    """
    date_stamp_start = json_data['list'][0]['dt']
    date_stamp_end = json_data['list'][-1]['dt']
    json_data['start_date'] = date_stamp_start
    json_data['end_date'] = date_stamp_end
    return json_data


def open_map_url(map_type, latitude, longitude):
    """
    Return the url to open the map on the web browser
    :param map_type: cloud/precipitation/windspeed/temperature
    :param latitude: float value of latitude
    :param longitude: float value of longitude
    :return: URL
    """
    params = urlencode(dict(basemap='map',
                            cities='true',
                            layer=map_type,
                            lat=latitude,
                            lon=longitude,
                            zoom=10))
    url = 'http://openweathermap.org/weathermap?{0}'.format(params)
    return url
