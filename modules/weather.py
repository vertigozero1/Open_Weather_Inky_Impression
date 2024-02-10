### Handles the actual API call to OpenWeather, and the parsing of the returned JSON data

import traceback    # for printing exceptions
import time         # for delaying prior to retrying failed calls
import sys          # for exiting upon fatal exception
import requests     # for making the OpenWeather API request

def get_data(apiKey, lati, long, out):
    """ Get weather data from the OpenWeather API, return data in custom object """

    endpoint = "https://api.openweathermap.org/data/3.0/onecall?"
    api_call_timeout = 60
    retry_delay = 60
    retry = False

    try:
        out.logger.info("Performing API call to %s", endpoint)
        url = endpoint + "lat=" + lati + "&lon=" + long + "&exclude=minutely,hourly&appid=" + apiKey + "&units=" + units
        response = requests.get(url, timeout=api_call_timeout)
        data = response.json()
    except Exception:
        out.logger.critical("Error getting weather data; will retry API call after %s seconds...", retry_delay)
        out.logger.critical(traceback.format_exc())
        retry=True
    finally:
        if retry:
            try:
                time.sleep(retry_delay)
                out.logger.info("Retrying API call...")
                response = requests.get(url, timeout=api_call_timeout)
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
    formatted_temp = f"{temp}0.0f"
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
