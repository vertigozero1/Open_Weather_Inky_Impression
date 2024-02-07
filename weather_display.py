
import traceback                # for printing exceptions
import time                     # for getting the current time
from datetime import datetime   # for converting the time to human-readable format

## Custom Modules
import modules.initialization as init
import modules.query_weather as owAPI

## Main Program
config = init.get_config()
out = init.start_logging(config.logLevel)
print("Log level: {config.logLevel}")

startTime = time.time()
startDatetime = datetime.fromtimestamp(startTime)
cleanStartTime = startDatetime.strftime('%Y-%m-%d %H:%M:%S')

out.logger.info("Starting weatherDisplay.py at {cleanStartTime}")
out.logger.debug(config)

city1Weather = owAPI.get_weather_data(config.apiKey, config.units, config.city1Lati, config.city1Long, out)

endTime = time.time()
duration = endTime - startTime
formattedDuration = "{:.2f}".format(duration)

out.logger.info("Ending weatherDisplay.py at {endTime}")
out.logger.info("Duration: {formattedDuration} seconds")
out.logger.info("=======================")

#from inky.auto import auto # for working with the e-ink display
#from PIL import Image, ImageFont, ImageDraw # for working with images
#import time # for sleeping between requests
#import datetime # for getting the current time

