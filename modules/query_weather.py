## Community Libraries
import requests     # for making the OpenWeather API request
import traceback    # for printing exceptions
import time         # for delaying prior to retrying failed calls
import sys          # for exiting upon fatal exception

def get_weather_data(apiKey, units, lati, long, out):
    """ Get weather data from the OpenWeather API, return data in custom object """
    
    endpoint = "https://api.openweathermap.org/data/3.0/onecall?"
    apiCallTimeout = 60
    retryDelay = 60

    try:
        out.logger.info("Performing API call to {endpoint}")
        url = endpoint + "lat=" + lati + "&lon=" + long + "&exclude=minutely,hourly&appid=" + apiKey + "&units=" + units
        response = requests.get(url, timeout=apiCallTimeout)
        data = response.json()
    except Exception:
        out.logger.critical("Error getting weather data; will retry API call after {retryDelay} seconds...")
        out.logger.critical(traceback.format_exc())
        retry=True
    finally:
        if retry:
            try:
                time.sleep(retryDelay)
                out.logger.info("Retrying API call...")
                response = requests.get(url, timeout=apiCallTimeout)
                data = response.json()
            except Exception:
                out.logger.critical("Weather data collection failed a second time! Exiting program.")
                out.logger.critical(traceback.format_exc())
                sys.exit

    out.logger.debug("Weather data: " + str(data))
    return data

def weather_css(data, out):
    """ Create CSS from the queried weather data. """

    try:
        code = data['current']['weather'][0]['id']
        weather = data['current']['weather'][0]['description']
        temp = data['current']['temp']
        feels_like = data['current']['feels_like']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_speed']
        wind_direction = data['current']['wind_deg']
        sunrise = data['current']['sunrise']
        sunset = data['current']['sunset']

        out.logger.debug("Weather code  : {code}")
        out.logger.debug("Weather       : {weather}")
        out.logger.debug("Temp          : {temp}")
        out.logger.debug("Feels like    : {feels_like}")
        out.logger.debug("Humidity      : {humidity}")
        out.logger.debug("Wind speed    : {wind_speed}")
        out.logger.debug("Wind direction: {wind_direction}")
        out.logger.debug("Sunrise       : {sunrise}")
        out.logger.debug("Sunset        : {sunset}")
    except Exception:
        out.logger.critical("Error parsing weather data")
        out.logger.critical(traceback.format_exc())
        sys.exit
    return
