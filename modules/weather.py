## Community Libraries
import requests     # for making the OpenWeather API request
import traceback    # for printing exceptions
import time         # for delaying prior to retrying failed calls
import sys          # for exiting upon fatal exception

def get_data(apiKey, units, lati, long, out):
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

def log_data(data, out):
    """ Log the weather data for debugging purposes """
    out.logger.debug("Weather icon  : %s", data.icon)
    out.logger.debug("Summary       : %s", data.summary)
    out.logger.debug("Weather       : %s", data.weather)
    out.logger.debug("Temp          : %s", data.temp)
    out.logger.debug("Feels like    : %s", data.feels_like)
    out.logger.debug("Humidity      : %s", data.humidity)
    out.logger.debug("Wind speed    : %s", data.wind_speed)
    out.logger.debug("Wind direction: %s", data.wind_direction)

def format_temp(temp):
    """ Format temperature to remove extra decimal places and negative zero """
    formattedTemp = "%0.0f" % temp
    if formattedTemp != "-0":
        return formattedTemp
    else:
        return "0"

class WeatherData:
    """ Custom object to store the weather data we're interested in """
    def __init__(self, name, data):
        self.name = name
        self.summary = str(data['current']['weather'][0]['main'])
        self.id = data['current']['weather'][0]['id']
        self.weather = data['current']['weather'][0]['description']
        self.temp = format_temp(data['current']['temp'])
        self.feels_like = format_temp(data['current']['feels_like'])
        self.humidity = data['current']['humidity']
        self.wind_speed = data['current']['wind_speed']
        self.wind_direction = data['current']['wind_deg']
        if 200 <= self.id < 300:
            self.icon = 'wi-thunderstorm'
        elif 300 <= self.id < 500:
            self.icon =  'wi-showers'
        elif 500 <= self.id < 600:
            self.icon =  'wi-rain'
        elif 600 <= self.id < 700:
            self.icon =  'wi-snow'
        elif 700 <= self.id < 800:
            self.icon =  'wi-fog'
        elif self.id == 800:
            self.icon =  'wi-day-sunny'
        elif self.id > 800:
            self.icon =  'wi-cloudy'

def generate_html(city_one_name, city_one_weather, out, city_two_name = None, city_two_weather = None):
    """ Create page from the queried weather data. """

    out.logger.debug("Generating HTML from weather data")

    date = time.strftime("%B %-d", time.localtime())
    weekday = time.strftime("%a", time.localtime())
    load_time = time.strftime("%-I:%M %p", time.localtime())

    html = '<!DOCTYPE html>\n'
    html += '<html>\n'
    html += ' <head>\n'
    #html += '  <link rel="stylesheet" href="css\weather-icons.css">\n'
    html += '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
    html += '  <style>\n'
    html += '   * { box-sizing: border-box; }\n'
    html += '   .column {\n'
    html += '   float: left;\n'
    html += '   width: 50%;\n'
    html += '   padding: 10px; }\n'
    html += '   .row:after {\n'
    html += '   content: "";\n'
    html += '   display: table;\n'
    html += '   clear: both; }\n'
    html += '  </style>\n'
    html += '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/weather-icons/2.0.10/css/weather-icons.min.css">\n'
    html += '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/weather-icons/2.0.10/css/weather-icons-wind.min.css">\n'
    html += ' </head>\n'
    html += '<body>\n'
    html += ' <div class="row">\n'
    html += f' <h1>{weekday}, {date}</h1>\n'
    html += f' <h2>Weather at {load_time}</h2>\n'
    html += '  <div class="column">\n'
    html += f'   <p>{city_one_name}</p>\n'
    html += f'   <i class="wi {city_one_weather.icon}"></i><br>\n'
    html += f'   <p>{city_one_weather.summary}</p>\n'
    html += f'   <p>{city_one_weather.weather}</p>\n'
    html += f'   <p>Temp: {city_one_weather.temp}°F</p>\n'
    html += f'   <p>Feels like: {city_one_weather.feels_like}°F</p>\n'
    html += f'   <p>Humidity: {city_one_weather.humidity}%</p>\n'
    html += f'   <p>Wind: {city_one_weather.wind_speed} mph</p>\n'
    html += f'   <p>Wind direction: {city_one_weather.wind_direction}°</p>\n'
    html += '  </div>\n'
    if city_two_weather:
        html += '  <div class="column">\n'
        html += f'   <p>{city_two_name}</p>\n'
        html += f'   <i class="wi {city_two_weather.icon}"></i><br>\n'
        html += f'   <p>{city_two_weather.summary}</p>\n'
        html += f'   <p>{city_two_weather.weather}</p>\n'
        html += f'   <p>Temp: {city_two_weather.temp}°F</p>\n'
        html += f'   <p>Feels like: {city_two_weather.feels_like}°F</p>\n'
        html += f'   <p>Humidity: {city_two_weather.humidity}%</p>\n'
        html += f'   <p>Wind: {city_two_weather.wind_speed} mph</p>\n'
        html += f'   <p>Wind direction: {city_two_weather.wind_direction}°</p>\n'
        html += '  </div>\n'
    html += ' </div>\n'
    html += '</body>\n'
    html += '</html>\n'
    out.logger.debug("HTML: %s", html)
    return html