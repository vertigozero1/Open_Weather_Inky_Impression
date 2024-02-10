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
    out.logger.debug("Weather data:")
    out.logger.debug("Summary       : %s", data.daily[0].summary)
    out.logger.debug("Weather       : %s", data.current.weather)
    out.logger.debug("Temp          : %s", data.current.temp)
    out.logger.debug("Feels like    : %s", data.current.feels_like)
    out.logger.debug("Humidity      : %s", data.current.humidity)
    out.logger.debug("Wind speed    : %s", data.current.wind_speed)
    out.logger.debug("Wind direction: %s", data.current.wind_deg)

def format_temp(temp):
    """ Format temperature to remove extra decimal places and negative zero """
    formatted_temp = "%0.0f" % temp
    if formatted_temp != "-0":
        return formatted_temp
    else:
        return "0"

class WeatherData:
    """ Custom object to store the weather data returned by the API call """
    def __init__(self, json_response):
        self.lat = json_response['lat']
        self.lon = json_response['lon']
        self.timezone = json_response['timezone']
        self.timezone_offset = json_response['timezone_offset']
        self.current = self._parse_current(json_response['current'])
        self.daily = [self._parse_daily(daily) for daily in json_response['daily']]
    
    def _parse_current(self, current_data):
        current = CurrentWeather()
        current.dt = current_data['dt']
        current.sunrise = current_data['sunrise']
        current.sunset = current_data['sunset']
        current.temp = current_data['temp']
        current.feels_like = current_data['feels_like']
        current.pressure = current_data['pressure']
        current.humidity = current_data['humidity']
        current.dew_point = current_data['dew_point']
        current.uvi = current_data['uvi']
        current.clouds = current_data['clouds']
        current.visibility = current_data['visibility']
        current.wind_speed = current_data['wind_speed']
        current.wind_deg = current_data['wind_deg']
        current.weather = self._parse_weather(current_data['weather'])
        return current
    
    def _parse_daily(self, daily_data):
        daily = DailyWeather()
        daily.dt = daily_data['dt']
        daily.sunrise = daily_data['sunrise']
        daily.sunset = daily_data['sunset']
        daily.moonrise = daily_data['moonrise']
        daily.moonset = daily_data['moonset']
        daily.moon_phase = daily_data['moon_phase']
        daily.summary = daily_data['summary']
        daily.temp = self._parse_temp(daily_data['temp'])
        daily.feels_like = self._parse_feels_like(daily_data['feels_like'])
        daily.pressure = daily_data['pressure']
        daily.humidity = daily_data['humidity']
        daily.dew_point = daily_data['dew_point']
        daily.wind_speed = daily_data['wind_speed']
        daily.wind_deg = daily_data['wind_deg']
        daily.wind_gust = daily_data['wind_gust']
        daily.weather = self._parse_weather(daily_data['weather'])
        daily.clouds = daily_data['clouds']
        daily.pop = daily_data['pop']
        daily.uvi = daily_data['uvi']
        return daily
    
    def _parse_temp(self, temp_data):
        temp = Temperature()
        temp.day = temp_data['day']
        temp.min = temp_data['min']
        temp.max = temp_data['max']
        temp.night = temp_data['night']
        temp.eve = temp_data['eve']
        temp.morn = temp_data['morn']
        return temp
    
    def _parse_feels_like(self, feels_like_data):
        feels_like = FeelsLike()
        feels_like.day = feels_like_data['day']
        feels_like.night = feels_like_data['night']
        feels_like.eve = feels_like_data['eve']
        feels_like.morn = feels_like_data['morn']
        return feels_like
    
    def _parse_weather(self, weather_data):
        weather = Weather()
        weather.id = weather_data[0]['id']
        weather.main = weather_data[0]['main']
        weather.description = weather_data[0]['description']
        weather.icon = weather_data[0]['icon']
        return weather

class CurrentWeather:
    pass

class DailyWeather:
    pass

class Temperature:
    pass

class FeelsLike:
    pass

class Weather:
    pass

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