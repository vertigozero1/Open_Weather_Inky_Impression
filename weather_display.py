"""
  ┳  ┓   ┏┓      ┓ ┏     ┓       ┏┓    •    
┏┓┃┏┓┃┏  ┃┃┏┓┏┓┏┓┃┃┃┏┓┏┓╋┣┓┏┓┏┓  ┗┓╋┏┓╋┓┏┓┏┓
┗ ┻┛┗┛┗  ┗┛┣┛┗ ┛┗┗┻┛┗ ┗┻┗┛┗┗ ┛   ┗┛┗┗┻┗┗┗┛┛┗
-----------┛--------------------------------                              
for Raspberry Pi and Pimoroni Inky Impression 7.3" e-ink display
"""
### Community Libraries
import time                     # for getting the current time
from datetime import datetime   # for converting the time to human-readable format
import os                       # for changing the working directory

### Custom Modules
import modules.initialization as init  # handles configuration and logging
import modules.weather as weather      # handles querying the OpenWeather API
import modules.render as img           # handles rendering HTML to image

### Main Program

## Initialize
os.chdir("/home/pi/Open_Weather_Inky_Impression/") # Project root

init.check_dependencies()
config = init.get_config()
out = init.start_logging(config.log_level)

start_time = time.time()
start_datetime = datetime.fromtimestamp(start_time)
formatted_start_time = start_datetime.strftime('%Y-%m-%d %H:%M:%S')

city_one_name = config.city_one_name

out.logger.info("Starting weatherDisplay.py at %s", formatted_start_time)
out.logger.debug(config)

## Get weather data
out.logger.info("Getting weather data for %s", city_one_name)
city_one_data = weather.get_data(config.api_key, config.city_one_lat, config.city_one_lon, out)
weather_one = weather.WeatherData(city_one_data)
weather.log_data(weather_one, out)

weather_two = None
if config.mode == "dual":
    out.logger.info("Getting weather data for %s", config.city_two_name)
    city_two_name = config.city_two_name
    city_two_data = weather.get_data(
        config.api_key,
        config.city_two_lat,
        config.city_two_lon,
        out)
    weather_two = weather.WeatherData(city_two_data)
    weather.log_data(weather_two, out)

img.render_pil(city_one_name, weather_one, out, city_two_name, weather_two)

end_time = time.time()
duration = end_time - start_time
formatted_duration = f"{duration:.2f}"

out.logger.info("Ending weatherDisplay.py at %s", end_time)
out.logger.info("Duration: %s seconds", formatted_duration)
out.logger.info("=======================")
