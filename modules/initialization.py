import configparser # for reading the config file
import logging      # for logging errors
import traceback    # for printing exceptions
import sys          # for logging to stdout

def interpret_log_level(logLevel):
    """ Given a log level string, returns the corresponding log level integer from the logging library """
    return {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
        }.get(logLevel.upper(), logging.WARNING) # default to WARNING if the log level is not recognized


def get_config():
    """ Import the config file and return the data object """
    try:
        raw_config = configparser.ConfigParser()
        raw_config.read('config.ini')
    except FileNotFoundError:
        print("Error reading config file")
        traceback.print_exc()
        exit(1)
    
    try:
        class config:
            def __init__(self):
                configLogLevel = raw_config.get('APPLICATION', 'logLevel', fallback='WARNING')
                self.logLevel = interpret_log_level(configLogLevel)

                self.apiKey = raw_config['OPENWEATHER']['apiKey']
                
                self.units = raw_config['OPENWEATHER']['units']            

                self.city1Name = raw_config['OPENWEATHER']['city1Name']
                self.city1Lati = raw_config['OPENWEATHER']['city1Lati']
                self.city1Long = raw_config['OPENWEATHER']['city1Long']

                if raw_config['OPENWEATHER']['city2Lati'] != 'latitude':
                    self.mode = 'dual'
                    self.city2Name = raw_config['OPENWEATHER']['city2Name']
                    self.city2Lati = raw_config['OPENWEATHER']['city2Lati']
                    self.city2Long = raw_config['OPENWEATHER']['city2Long']
                else:
                    self.mode = 'single'
    except Exception:
        print("Error parsing config file")
        traceback.print_exc()
        exit(1)
        
    output = config()
    return output


def start_logging(logLevel):
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
