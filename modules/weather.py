""" Handles the actual API call to OpenWeather, and the parsing of the returned JSON data """

import traceback                                    # for printing exceptions
import time                                         # for delaying prior to retrying failed calls
import sys                                          # for exiting upon fatal exception
from datetime import datetime                       # for formatting the time
import requests                                     # for making the OpenWeather API request
import numpy as np                                  # for linear regression
from sklearn.linear_model import LinearRegression   # for trend analysis
                                                    #   https://scikit-learn.org/stable/install.html
                                                    #   pip3 install scikit-learn`

### MODULE FUNCTIONS

def get_data(api_key, lati, long, out):
    """ Get weather data from the OpenWeather API, return data in custom object """

    endpoint = "https://api.openweathermap.org/data/3.0/onecall?"
    api_call_timeout = 60
    retry_delay = 60
    retry = False

    try:
        out.logger.info("Performing API call to %s", endpoint)

        lat_long = "lat=" + lati + "&lon=" + long
        appid = "&appid=" + api_key
        exclude = "&exclude=minutely"
        units = "&units=imperial"
        url = endpoint + lat_long + exclude + appid + units

        response = requests.get(url, timeout=api_call_timeout)
        data = response.json()
    except Exception:
        message = "Error getting weather data; will retry API call after %s seconds..."
        out.logger.critical(message, retry_delay)
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
                message = "Weather data collection failed a second time! Exiting program."
                out.logger.critical(message)
                out.logger.critical(traceback.format_exc())
                sys.exit()

    out.logger.debug("Weather data: %s", data)
    return data

def log_data(data, out):
    """ Log some general weather data for debugging purposes """
    out.logger.info("Weather data received")
    out.logger.debug(f"{data.lat}, {data.lon}, {data.timezone}, {data.timezone_offset}")
    out.logger.debug(f"{data.current.weather.description}")
    out.logger.debug(f"Temperature: {data.current.temp}, Feels Like: {data.current.feels_like}")
    out.logger.debug(f"Pressure: {data.current.pressure}, Humidity: {data.current.humidity}")
    out.logger.debug(f"Dew Point: {data.current.dew_point}, UVI: {data.current.uvi}")
    out.logger.debug(f"Clouds: {data.current.clouds}, Visibility: {data.current.visibility}")
    out.logger.debug(f"Wind: {data.current.wind_description}")
    out.logger.debug(f"Sunrise: {data.current.sunrise}, Sunset: {data.current.sunset}")
    return

def format_temp(temp):
    """ Format temperature to remove extra decimal places and negative zero """
    try:
        temp = float(temp)
    except ValueError:
        temp = -99
    formatted_temp = f"{temp:.0f}"
    if formatted_temp == "-0":
        return "0"
    else:
        return formatted_temp

def format_clocktime(dt):
    """ Format the time to remove seconds """
    formatted_time = datetime.fromtimestamp(dt).strftime('%I:%M %p')
    return formatted_time

def get_compass_direction(degrees):
    """ Convert degrees to textual compass direction """
    directions = ['N', 'NNE', 'NE', 'ENE',
                  'S', 'SSW', 'SW', 'WSW',
                  'E', 'ESE', 'SE', 'SSE',
                  'W', 'WNW', 'NW', 'NNW']
    index = round(degrees / 22.5) % 16
    return directions[index]

def identify_trend(data_list):
    """ Identify the trending direction of the given attribute """
    i = 0
    x = []
    y = data_list

    for iteration in data_list:
        i += 1
        x.append(i)
        #print(f"x: {i}, y: {iteration}")

    x_array = np.array(x)
    reshaped_x = x_array.reshape(-1, 1)

    model = LinearRegression().fit(reshaped_x, y)

    trend = TrendInfo()

    trend.slope = model.coef_
    trend.intercept = model.intercept_
    trend.r_value = model.score(reshaped_x, y)
    trend.no_slope = trend.slope == 0
    trend.positive_trend = trend.slope > 0
    trend.direction = "up" if trend.positive_trend else "down"
    if trend.slope > 2 or trend.slope < -2:
        trend.steep = True
    else:
        trend.steep = False

    return trend

### CLASS DECLARATIONS

class TrendInfo:
    """ Custom object to store the trend information """
    def __init__(self):
        self.trend = None
        self.slope = None
        self.intercept = None
        self.r_value = None
        self.positive_trend = None
        self.direction = None
        self.steep = None
        self.no_slope = None

class WeatherData:
    """ Custom object to store the weather data returned by the API call """
    def __init__(self, json_response):
        self.lat = json_response['lat']
        self.lon = json_response['lon']
        self.timezone = json_response['timezone']
        self.timezone_offset = json_response['timezone_offset']
        self.current = self._parse_current(json_response['current'])
        self.daily = [self._parse_daily(daily) for daily in json_response['daily']]
        self.hourly = [self._parse_hourly(hourly) for hourly in json_response['hourly']]

    def _parse_current(self, current_data):
        current = CurrentWeather()
        current.dt = current_data['dt']
        current.sunrise = current_data['sunrise']
        current.sunset = current_data['sunset']
        current.temp = format_temp(current_data['temp'])
        current.feels_like = format_temp(current_data['feels_like'])
        current.pressure = f"{current_data['pressure']} hPa"
        current.humidity = f"{current_data['humidity']:.0f}%"
        current.humidity_raw = current_data['humidity']
        current.dew_point = format_temp(current_data['dew_point'])
        current.uvi = current_data['uvi']
        current.clouds = f"{current_data['clouds']:.0f}%"
        current.visibility = f"{current_data['visibility']/100:.0f}%"
        current.wind_speed = current_data['wind_speed']
        current.wind_deg = current_data['wind_deg']
        current.wind_dir = get_compass_direction(current_data['wind_deg'])
        current.wind_description = f"{current.wind_speed}mph {current.wind_dir}"
        current.weather = self._parse_weather(current_data['weather'])
        return current

    def _parse_daily(self, daily_data):
        daily = DailyWeather()
        daily.dt = daily_data['dt']
        daily.day = datetime.fromtimestamp(daily_data['dt']).strftime('%A')
        daily.day_of_month = datetime.fromtimestamp(daily_data['dt']).strftime('%d')
        daily.month = datetime.fromtimestamp(daily_data['dt']).strftime('%B')
        daily.sunrise = format_clocktime(daily_data['sunrise'])
        daily.sunset = format_clocktime(daily_data['sunset'])
        daily.moonrise = format_clocktime(daily_data['moonrise'])
        daily.moonset = format_clocktime(daily_data['moonset'])
        daily.moon_phase = daily_data['moon_phase']
        daily.summary = daily_data['summary']
        daily.temp = self._parse_temp(daily_data['temp'])
        daily.feels_like = self._parse_feels_like(daily_data['feels_like'])
        daily.pressure = f"{daily_data['pressure']} hPa"
        daily.humidity = f"{daily_data['humidity']:.0f}%"
        daily.raw_humidity = daily_data['humidity']
        daily.dew_point = format_temp(daily_data['dew_point'])
        daily.wind_speed = daily_data['wind_speed']
        daily.wind_deg = daily_data['wind_deg']
        daily.wind_dir = get_compass_direction(daily_data['wind_deg'])
        daily.wind_description = f"{daily.wind_speed}mph {daily.wind_dir}"
        daily.wind_gust = daily_data['wind_gust']
        daily.weather = self._parse_weather(daily_data['weather'])
        daily.clouds = f"{daily_data['clouds']:.0f}%"
        daily.pop = f"{daily_data['pop']:.0%}"
        daily.pop_raw = daily_data['pop']
        daily.uvi = daily_data['uvi']
        return daily

    def _parse_hourly(self, hourly_data):
        hourly = HourlyWeather()
        hourly.dt = format_clocktime(hourly_data['dt'])
        hourly.temp_raw = hourly_data['temp']
        hourly.temp = format_temp(hourly_data['temp'])
        hourly.feels_like = format_temp(hourly_data['feels_like'])
        hourly.pressure = f"{hourly_data['pressure']} hPa"
        hourly.pressure_raw = hourly_data['pressure']
        hourly.humidity = f"{hourly_data['humidity']:.0f}%"
        hourly.humidity_raw = int(hourly_data['humidity'])
        hourly.dew_point = hourly_data['dew_point']
        hourly.uvi = hourly_data['uvi']
        hourly.clouds = f"{hourly_data['clouds']:.0f}%"
        hourly.visibility = f"{hourly_data['visibility']/100:.0f}%"
        hourly.wind_speed = hourly_data['wind_speed']
        hourly.wind_deg = hourly_data['wind_deg']
        hourly.wind_dir = get_compass_direction(hourly_data['wind_deg'])
        hourly.wind_description = f"{hourly.wind_speed}mph {hourly.wind_dir}"
        hourly.wind_gust = hourly_data['wind_gust']
        hourly.pop = f"{hourly_data['pop']:.0%}"
        hourly.pop_raw = int(hourly_data['pop'])
        hourly.weather = self._parse_weather(hourly_data['weather'])
        return hourly

    def _parse_temp(self, temp_data):
        temp = Temperature()
        temp.day_raw = int(temp_data['day'])
        temp.day = format_temp(temp_data['day'])
        temp.min = format_temp(temp_data['min'])
        temp.max = format_temp(temp_data['max'])
        temp.night = format_temp(temp_data['night'])
        temp.eve = format_temp(temp_data['eve'])
        temp.morn = format_temp(temp_data['morn'])
        return temp

    def _parse_feels_like(self, feels_like_data):
        feels_like = FeelsLike()
        feels_like.day_raw = int(feels_like_data['day'])
        feels_like.day = format_temp(feels_like_data['day'])
        feels_like.night = format_temp(feels_like_data['night'])
        feels_like.eve = format_temp(feels_like_data['eve'])
        feels_like.morn = format_temp(feels_like_data['morn'])
        return feels_like

    def _parse_weather(self, weather_data):
        weather_class = Weather()
        weather_class.id = weather_data[0]['id']
        weather_class.main = weather_data[0]['main']
        weather_class.description = weather_data[0]['description']
        weather_class.icon = weather_data[0]['icon']
        return weather_class

class CurrentWeather:
    """ Custom object to store the current weather data """
    def __init__(self):
        self.dt = None
        self.sunrise = None
        self.sunset = None
        self.temp = None
        self.temp_raw = None
        self.feels_like = None
        self.feels_like_raw = None
        self.pressure = None
        self.humidity = None
        self.humidity_raw = None
        self.dew_point = None
        self.uvi = None
        self.clouds = None
        self.visibility = None
        self.wind_speed = None
        self.wind_deg = None
        self.wind_dir = None
        self.wind_description = None
        self.weather = None

class DailyWeather:
    """ Custom object to store the daily weather data """
    def __init__(self):
        self.dt = None
        self.day = None
        self.day_of_month = None
        self.month = None
        self.sunrise = None
        self.sunset = None
        self.moonrise = None
        self.moonset = None
        self.moon_phase = None
        self.summary = None
        self.temp = None
        self.feels_like = None
        self.pressure = None
        self.humidity = None
        self.raw_humidity = None
        self.dew_point = None
        self.wind_speed = None
        self.wind_deg = None
        self.wind_dir = None
        self.wind_gust = None
        self.wind_description = None
        self.weather = None
        self.clouds = None
        self.pop = None
        self.pop_raw = None
        self.uvi = None

class HourlyWeather:
    """ Custom object to store the hourly weather data"""
    def __init__(self):
        self.dt = None
        self.temp = None
        self.temp_raw = None
        self.feels_like = None
        self.feels_like_raw = None
        self.pressure = None
        self.pressure_raw = None
        self.humidity = None
        self.humidity_raw = None
        self.dew_point = None
        self.uvi = None
        self.clouds = None
        self.visibility = None
        self.wind_speed = None
        self.wind_deg = None
        self.wind_dir = None
        self.wind_description = None
        self.wind_gust = None
        self.pop = None
        self.pop_raw = None
        self.weather = None

class Temperature:
    """ Custom object to store the temperature data """
    def __init__(self):
        self.day_raw = None
        self.day = None
        self.min = None
        self.max = None
        self.night = None
        self.eve = None
        self.morn = None

class FeelsLike:
    """ Custom object to store the feels_like data """
    def __init__(self):
        self.day_raw = None
        self.day = None
        self.night = None
        self.eve = None
        self.morn = None

class Weather:
    """ Custom object to store the weather data """
    def __init__(self):
        self.id = None
        self.main = None
        self.description = None
        self.icon = None