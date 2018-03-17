from datetime import datetime, timedelta

import matplotlib.dates as plot_dates
import matplotlib.pyplot as plotting

from utils import get_db


def mongo_data():
    """
    Retrieves the 10 days forecast data from database
    :return: Dictionary of 10 days weather forecast
    """
    db = get_db()
    start = datetime.today()
    end = datetime.today() + timedelta(days=5)
    params = {'start_date': {'$gte': int(start.timestamp())}, 'end_date': {'$lt': int(end.timestamp())}}
    data_from_db = db.fiveDayUpdate.find(params)
    for d in data_from_db:
        return d


def plot_data():
    """
    The date and the corresponding temperature data are appended to the empty list.
    The temperature is converted from K to F
    :return: The date data list and corresponding weather temperature list
    """
    date_list = []
    temp_list = []
    data = mongo_data()
    for reading in data['list']:
        date = datetime.fromtimestamp(int(reading['dt']))
        temperature = 1.8 * reading['main']['temp'] - 459.67
        date_list.append(date)
        temp_list.append(temperature)
        print('{0} : {1}'.format(date, temperature))
    return date_list, temp_list


def plot_graph():
    """
    Plot a graph of temperature vs date
    """
    date_list, temp_list = plot_data()
    fig, ax = plotting.subplots()
    ax.plot_date(date_list, temp_list, '-')
    ax.grid(True)

    # format x-axis dates
    plotting.xticks(rotation='horizontal')
    date_format = plot_dates.DateFormatter('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(date_format)
    plotting.show()


if __name__ == '__main__':
    plot_graph()
