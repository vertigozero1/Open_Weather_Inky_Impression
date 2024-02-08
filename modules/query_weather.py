## Community Libraries
import requests     # for making the OpenWeather API request
import traceback    # for printing exceptions
import time         # for delaying prior to retrying failed calls
import sys          # for exiting upon fatal exception

def map_weather_code(code):
    """ Map weather codes to weather icons for CSS """
    if 200 <= code < 300:
        return 'wi-thunderstorm'
    elif 300 <= code < 500:
        return 'wi-showers'
    elif 500 <= code < 600:
        return 'wi-rain'
    elif 600 <= code < 700:
        return 'wi-snow'
    elif 700 <= code < 800:
        return 'wi-fog'
    elif code == 800:
        return 'wi-day-sunny'
    elif code > 800:
        return 'wi-cloudy'

def get_weather_data(apiKey, units, lati, long, out):
    """ Get weather data from the OpenWeather API, return data in custom object """
    
    endpoint = "https://api.openweathermap.org/data/3.0/onecall?"
    apiCallTimeout = 60
    retryDelay = 60
    retry = False

    try:
        out.logger.info("Performing API call to %s", endpoint)
        url = endpoint + "lat=" + lati + "&lon=" + long + "&exclude=minutely,hourly&appid=" + apiKey + "&units=" + units
        response = requests.get(url, timeout=apiCallTimeout)
        data = response.json()
    except Exception:
        out.logger.critical("Error getting weather data; will retry API call after %s seconds...", retryDelay)
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

    out.logger.debug("Weather data: %s", data)
    return data

def log_weather_data(data, out):
        out.logger.debug("Weather icon  : %s", data.icon)
        out.logger.debug("Weather       : %s", data.weather)
        out.logger.debug("Temp          : %s", data.temp)
        out.logger.debug("Feels like    : %s", data.feels_like)
        out.logger.debug("Humidity      : %s", data.humidity)
        out.logger.debug("Wind speed    : %s", data.wind_speed)
        out.logger.debug("Wind direction: %s", data.wind_direction)
        out.logger.debug("Sunrise       : %s", data.sunrise)
        out.logger.debug("Sunset        : %s", data.sunset)

def generate_weather_html(data, out, data2 = None):
    """ Create page from the queried weather data. """
    out.logger.debug("Generating HTML from weather data")
    weather_one = None
    weather_two = None
    
    try:
        class WeatherData:
            def __init__(self, data):
                self.weather = data['current']['weather'][0]['description']
                self.temp = data['current']['temp']
                self.feels_like = data['current']['feels_like']
                self.humidity = data['current']['humidity']
                self.wind_speed = data['current']['wind_speed']
                self.wind_direction = data['current']['wind_deg']
                self.sunrise = data['current']['sunrise']
                self.sunset = data['current']['sunset']
                self.icon = map_weather_code(data['current']['weather'][0]['id'])

        log_weather_data(data, out)

        weather_one = WeatherData(data)
        if data2:
            weather_two = WeatherData(data2)
            log_weather_data(data2, out)
    except Exception:
        out.logger.critical("Error parsing weather data")
        out.logger.critical(traceback.format_exc())
        sys.exit

    html = '<div class="row">'
    html += ' <div class="column">'
    html += f'  <i class="wi {weather_one.icon}"></i><br>'
    html += f'  <p>{weather_one.weather}</p>'
    html += f'  <p>Temp: {weather_one.temp}°F</p>'
    html += f'  <p>Feels like: {weather_one.feels_like}°F</p>'
    html += f'  <p>Humidity: {weather_one.humidity}%</p>'
    html += f'  <p>Wind: {weather_one.wind_speed} mph</p>'
    html += f'  <p>Wind direction: {weather_one.wind_direction}°</p>'
    html += f'  <p>Sunrise: {weather_one.sunrise}</p>'
    html += f'  <p>Sunset: {weather_one.sunset}</p>'
    html += ' </div>'
    if data2:
        html += ' <div class="column">'
        html += f'  <i class="wi {weather_two.icon}"></i><br>'
        html += f'  <p>{weather_two.weather}</p>'
        html += f'  <p>Temp: {weather_two.temp}°F</p>'
        html += f'  <p>Feels like: {weather_two.feels_like}°F</p>'
        html += f'  <p>Humidity: {weather_two.humidity}%</p>'
        html += f'  <p>Wind: {weather_two.wind_speed} mph</p>'
        html += f'  <p>Wind direction: {weather_two.wind_direction}°</p>'
        html += f'  <p>Sunrise: {weather_two.sunrise}</p>'
        html += f'  <p>Sunset: {weather_two.sunset}</p>'
        html += ' </div>'
    html += '</div>'
    out.logger.debug("HTML: %s", html)
    return html