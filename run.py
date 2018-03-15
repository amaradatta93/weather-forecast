import datetime
import threading
import time
import webbrowser

from config import LOCATIONS, REFRESH_FREQUENCY_FORECAST, REFRESH_FREQUENCY_CURRENT
from utils import push_data_to_db, api_url_json, add_field, open_map_url


def five_day_forecast():
    while True:
        for location in LOCATIONS:
            zipcode = LOCATIONS[location]['zip']
            hour = 'forecast'
            json_data_hourly = api_url_json(hour, zipcode)
            formatted_hourly = json_data_hourly['list'][0]['weather'][0]['main']
            time_forecast = json_data_hourly['list'][0]['dt_txt']
            push_data_to_db('fiveDayUpdate', add_field(json_data_hourly))
            if formatted_hourly != 'Clear':
                print('{0:>27}: {1:>20}: {2} in {3}'.format(time_forecast, 'The weather will be', formatted_hourly,
                                                            location))
        time.sleep(REFRESH_FREQUENCY_FORECAST)


def current_forecast():
    while True:
        for location in LOCATIONS:
            zipcode = LOCATIONS[location]['zip']
            current = 'weather'
            json_data_current = api_url_json(current, zipcode)
            formatted_current = json_data_current['weather'][0]['main']
            current_weather_timestamp = datetime.datetime.now().isoformat()
            push_data_to_db('currentUpdate', json_data_current)
            print('{0:>27}: {1:>20}: {2} in {3}'.format(current_weather_timestamp, 'Current Weather',
                                                        formatted_current, location))
        time.sleep(REFRESH_FREQUENCY_CURRENT)


'''No access to 16 days/daily forecast so did for the current weather

def daily_f():
    while True:
        for zipcode in zip_input:
            daily = 'forecast/daily'
            json_data_daily = api_url_json(daily, zipcode)
            push_data_to_db('sixteenDayUpdate', add_field(json_data_daily))
            print(json_data_daily)
        time.sleep(2)
        
'''


def open_map(map_type):
    for location in LOCATIONS:
        latitude = LOCATIONS[location]['latitude']
        longitude = LOCATIONS[location]['longitude']
        url = open_map_url(map_type, latitude, longitude)
        webbrowser.open(url)


def main():
    print("""
The different types of maps you can access are:
clouds
precipitation
temperature
windspeed
    """)

    map_type = input("Choose from above: ")

    t1 = threading.Thread(target=five_day_forecast, args=())
    t2 = threading.Thread(target=current_forecast, args=())
    t3 = threading.Thread(target=open_map, args=(map_type,))
    # t4 = threading.Thread(target=daily_f, args=(zip_input,)) # access denied
    t1.start()
    t2.start()
    t3.start()
    # t4.start()


if __name__ == "__main__":
    main()
