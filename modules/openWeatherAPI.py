## Community Libraries
import requests     # for making the OpenWeather API request
import json         # for reading the OpenWeather API response
import traceback    # for printing exceptions

def getWeatherData(apiKey, units, lati, long, out):
    endpoint = "https://api.openweathermap.org/data/3.0/onecall?"
    try:
        url = endpoint + "lat=" + lati + "&lon=" + long + "&exclude=minutely,hourly&appid=" + apiKey + "&units=" + units
        response = requests.get(url)
        data = response.json()
    except:
        out.logger.critical("Error getting weather data")
        out.logger.critical(traceback.format_exc())
        exit(1)
    out.logger.debug("Weather data: " + str(data))
    return data

def weatherCSS(data, out):
    try:
        code = data['current']['weather'][0]['id']
        weather = data['current']['weather'][0]['description']
        temp = data['current']['temp']
        feelsLike = data['current']['feels_like']
        humidity = data['current']['humidity']
        windSpeed = data['current']['wind_speed']
        windDirection = data['current']['wind_deg']
        sunrise = data['current']['sunrise']
        sunset = data['current']['sunset']

        out.logger.debug("Weather: " + weather)
        out.logger.debug("Temp: " + str(temp))
        out.logger.debug("Feels like: " + str(feelsLike))
        out.logger.debug("Humidity: " + str(humidity))
        out.logger.debug("Wind speed: " + str(windSpeed))
        out.logger.debug("Wind direction: " + str(windDirection))
        out.logger.debug("Sunrise: " + str(sunrise))
        out.logger.debug("Sunset: " + str(sunset))
    except:
        out.logger.critical("Error parsing weather data")
        out.logger.critical(traceback.format_exc())
        exit(1)
    return