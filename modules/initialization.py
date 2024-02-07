import configparser # for reading the config file
import logging      # for logging errors
import traceback    # for printing exceptions
import logging      # for logging errors
import sys          # for logging to stdout

def interpretLogLevel(logLevel):
    """Given a log level string, returns the corresponding log level integer from the logging library"""
    return {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
        }.get(logLevel.upper(), logging.WARNING) # default to WARNING if the log level is not recognized


def getConfig():
    """Import the config file and return the data object"""
    try:
        rawConfig = configparser.ConfigParser()
        rawConfig.read('config.ini')
    except:
        print("Error reading config file")
        traceback.print_exc()
        exit(1)
    
    try:
        class config:
            def __init__(self):
                configLogLevel = rawConfig.get('APPLICATION', 'logLevel', fallback='WARNING')
                self.logLevel = interpretLogLevel(configLogLevel)

                self.apiKey = rawConfig['OPENWEATHER']['apiKey']
                
                self.units = rawConfig['OPENWEATHER']['units']            

                self.city1Name = rawConfig['OPENWEATHER']['city1Name']
                self.city1Lati = rawConfig['OPENWEATHER']['city1Lati']
                self.city1Long = rawConfig['OPENWEATHER']['city1Long']

                if rawConfig['OPENWEATHER']['city2Lati'] != 'latitude':
                    self.mode = 'dual'
                    self.city2Name = rawConfig['OPENWEATHER']['city2Name']
                    self.city2Lati = rawConfig['OPENWEATHER']['city2Lati']
                    self.city2Long = rawConfig['OPENWEATHER']['city2Long']
                else:
                    self.mode = 'single'
    except:
        print("Error parsing config file")
        traceback.print_exc()
        exit(1)
        
    output = config()
    return output


def startLogging(logLevel):
    """Set up logging for the main application, with a log object that can be passed to methods"""
    class track:
        def __init__(self):
            self.logger = logging.getLogger()
            self.logger.setLevel(logLevel)

            self.fileHandler = logging.FileHandler('weatherDisplay.log')
            self.fileHandler.setLevel(logLevel)

            self.stdoutHandler = logging.StreamHandler(sys.stdout)
            self.stdoutHandler.setLevel(logLevel)

            self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')

            self.fileHandler.setFormatter(self.formatter)
            self.stdoutHandler.setFormatter(self.formatter)

            self.logger.addHandler(self.fileHandler)
            self.logger.addHandler(self.stdoutHandler)
    output = track()
    return output