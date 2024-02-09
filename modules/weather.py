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
    """ Log the weather data """
    out.logger.debug("Weather icon  : %s", data.icon)
    out.logger.debug("Weather       : %s", data.weather)
    out.logger.debug("Temp          : %s", data.temp)
    out.logger.debug("Feels like    : %s", data.feels_like)
    out.logger.debug("Humidity      : %s", data.humidity)
    out.logger.debug("Wind speed    : %s", data.wind_speed)
    out.logger.debug("Wind direction: %s", data.wind_direction)
    out.logger.debug("Sunrise       : %s", data.sunrise)
    out.logger.debug("Sunset        : %s", data.sunset)

def format_temp(temp):
    formattedTemp = "%0.0f" % temp
    if formattedTemp != "-0":
        return formattedTemp
    else:
        return "0"

def generate_html(city1, data, out, city2 = None, data2 = None):
    """ Create page from the queried weather data. """

    out.logger.debug("Generating HTML from weather data")
    weather_one = None
    weather_two = None
    
    try:
        class WeatherData:
            def __init__(self, city, data):
                self.name = city
                self.summary = data['current']['summary']
                self.id = data['current']['weather'][0]['id']
                self.weather = data['current']['weather'][0]['description']
                self.temp = format_temp(data['current']['temp'])
                self.feels_like = format_temp(data['current']['feels_like'])
                self.humidity = data['current']['humidity']
                self.wind_speed = data['current']['wind_speed']
                self.wind_direction = data['current']['wind_deg']
                self.sunrise = data['current']['sunrise']
                self.sunset = data['current']['sunset']
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

        weather_one = WeatherData(city1, data)
        log_data(weather_one, out)

        if data2:
            weather_two = WeatherData(city2, data2)
            log_data(weather_two, out)
    except Exception:
        out.logger.critical("Error parsing weather data")
        out.logger.critical(traceback.format_exc())
        sys.exit

    date = time.strftime("%B %-d", time.localtime(epoch))
    weekday = time.strftime("%a", time.localtime(epoch))

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
    html += f' <h2>{date} {weekday}</h2>\n'
    html += f' <title>Weather at {time.time()}</title>\n'
    html += '  <div class="column">\n'
    html += f'   <p>{weather_one.name}</p>\n'
    html += f'   <i class="wi {weather_one.icon}"></i><br>\n'
    html += f'   <p>{weather_one.weather}</p>\n'
    html += f'   <p>Temp: {weather_one.temp}°F</p>\n'
    html += f'   <p>Feels like: {weather_one.feels_like}°F</p>\n'
    html += f'   <p>Humidity: {weather_one.humidity}%</p>\n'
    html += f'   <p>Wind: {weather_one.wind_speed} mph</p>\n'
    html += f'   <p>Wind direction: {weather_one.wind_direction}°</p>\n'
    html += f'   <p>Sunrise: {weather_one.sunrise}</p>\n'
    html += f'   <p>Sunset: {weather_one.sunset}</p>\n'
    html += '  </div>\n'
    if data2:
        html += '  <div class="column">\n'
        html += f'   <p>{weather_two.name}</p>\n'
        html += f'   <i class="wi {weather_two.icon}"></i><br>\n'
        html += f'   <p>{weather_two.weather}</p>\n'
        html += f'   <p>Temp: {weather_two.temp}°F</p>\n'
        html += f'   <p>Feels like: {weather_two.feels_like}°F</p>\n'
        html += f'   <p>Humidity: {weather_two.humidity}%</p>\n'
        html += f'   <p>Wind: {weather_two.wind_speed} mph</p>\n'
        html += f'   <p>Wind direction: {weather_two.wind_direction}°</p>\n'
        html += f'   <p>Sunrise: {weather_two.sunrise}</p>\n'
        html += f'   <p>Sunset: {weather_two.sunset}</p>\n'
        html += '  </div>\n'
    html += ' </div>\n'
    html += '</body>\n'
    html += '</html>\n'
    out.logger.debug("HTML: %s", html)
    return html