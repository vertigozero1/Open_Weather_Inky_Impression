
import traceback    # for printing exceptions
import imgkit       # for converting CSS/HTML to an image
import time         # for getting the current time
from datetime import datetime     # for converting the time to human-readable format

## Custom Modules
import modules.initialization as init
import modules.openWeatherAPI as owAPI

## Main Program
config = init.getConfig()
out = init.startLogging(config.logLevel)
print("Log level: " + str(config.logLevel))

startTime = time.time()
startDatetime = datetime.fromtimestamp(startTime)
cleanStartTime = startDatetime.strftime('%Y-%m-%d %H:%M:%S')

out.logger.info("Starting weatherDisplay.py at " + str(cleanStartTime))
out.logger.debug(config)

city1Weather = owAPI.getWeatherData(config.apiKey, config.units, config.city1Lati, config.city1Long, out)



endTime = time.time()
duration = endTime - startTime
formattedDuration = "{:.2f}".format(duration)

out.logger.info("Ending weatherDisplay.py at " + str(endTime))
out.logger.info("Duration: " + str(formattedDuration) + " seconds")
out.logger.info("====================================================")

#from inky.auto import auto # for working with the e-ink display
#from PIL import Image, ImageFont, ImageDraw # for working with images
#import time # for sleeping between requests
#import datetime # for getting the current time

