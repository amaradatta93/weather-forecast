The following is a script to get the weather forecast from www.openweathermap.com. The data obtained is plotted using matplotlib and stored in the mongodb. 

# Setup
1. Clone the repository
2. Create a virtual environment using: `virtualenv env`
3. Activate virtual env: `source env/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. `export BROWSER=google-chrome`
6. `export WEATHER_API_KEY={your OpenWeatherMap API key}`
7. Start MongoDB

# Run
1. Run the forecast: `python run.py`
2. run the plot: `python plotting.py`

# Configuration
1. Add locations in config.py using the following format:
	``` 'City name': {'latitude': latitude, 'longitude': longitude, 'zip': 5-digit zip_code} ```

2. Change the refresh frequency (in seconds) of 5 days/3 hour by altering REFRESH_FREQUENCY_FORECAST
3. Change the refresh frequency (in seconds) of current weather date by altering REFRESH_FREQUENCY_CURRENT
4. Use `ctrl + c` to quit anytime

# Note
Access to 16days/daily forecast is not avalable for free API keys
