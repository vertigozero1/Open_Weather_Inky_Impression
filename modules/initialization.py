### This module is responsible for setting up the application, including reading the config file, setting up logging, and interpreting the log level from the config file
import logging      # for logging errors
import traceback    # for printing exceptions
import sys          # for logging to stdout
import configparser # for reading the config file
import subprocess   # for running pip commands
import pip          # for installing missing packages

def import_or_install(package, alt_package_name=None):
    """ 
    Import a package, or install it if not found 
    
    Args:
        package (str): The name of the package to import or install.
        alt_package_name (str, optional): An alternate package name to 
                                          install if the main package is not found.

    Raises:
        ImportError: If the package cannot be imported.
        Exception: If there is an error installing the package or the alternate package.
    
    """
    try:
        __import__(package)
    except ImportError:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except Exception:
            print(f"Error installing package {package}")
            traceback.print_exc()
            if alt_package_name != "None":
                try:
                    pip.main(['install', alt_package_name])
                except Exception:
                    print(f"Error installing alternate package {alt_package_name}")
                    traceback.print_exc()
                    sys.exit()

def check_dependencies():
    """ Check for required packages and install them if missing """
    import_or_install('requests')
    import_or_install('PIL', 'Pillow')
    import_or_install('numpy')
    import_or_install('scikit-learn')
    import_or_install('inky', 'inky[rpi,example-depends]')

def interpret_log_level(log_level):
    """ Given a log level string, returns the corresponding 
        log level integer from the logging library """
    return {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
        # default to WARNING if the log level is not recognized
        }.get(log_level.upper(), logging.WARNING)

def get_config():
    """Import the config file and return the data object.
    
    Reads the 'config.ini' file and extracts the necessary configuration data.
    The function returns a data object containing the configuration values.

    Returns:
        config: A data object containing the configuration values.

    Raises:
        FileNotFoundError: If the 'config.ini' file is not found.
        Exception: If there is an error parsing the config file.
    """
    try:
        raw_config = configparser.ConfigParser()
        raw_config.read('config.ini')
    except FileNotFoundError:
        print("Error reading config file")
        traceback.print_exc()
        sys.exit()

    try:
        class Config:
            ### Custom object to hold the configuration data
            def __init__(self):
                config_log_level = raw_config.get('APPLICATION', 'logLevel', fallback='WARNING')
                self.log_level = interpret_log_level(config_log_level)

                self.api_key = raw_config['OPENWEATHER']['apiKey']

                self.city_one_name = raw_config['OPENWEATHER']['city1Name']
                self.city_one_lat = raw_config['OPENWEATHER']['city1Lati']
                self.city_one_lon = raw_config['OPENWEATHER']['city1Long']

                if raw_config['OPENWEATHER']['city2Lati'] != 'latitude':
                    self.mode = 'dual'
                    self.city_two_name = raw_config['OPENWEATHER']['city2Name']
                    self.city_two_lat = raw_config['OPENWEATHER']['city2Lati']
                    self.city_two_lon = raw_config['OPENWEATHER']['city2Long']
                else:
                    self.mode = 'single'
    except Exception:
        print("Error parsing config file")
        traceback.print_exc()
        exit(1)

    output = Config()
    return output


def start_logging(log_level):
    """Set up logging for the main application, with a log object that can be passed to methods

    Args:
        log_level (int): The log level to be set for the logger and handlers.

    Returns:
        Track: An instance of the Track class that holds the logger 
               and handlers for application runtime data tracking.
    """
    class Track:
        """ A class to hold the logger and handlers for application runtime data tracking """

        def __init__(self):
            self.logger = logging.getLogger()
            self.logger.setLevel(log_level)

            self.file_handler = logging.FileHandler('weatherDisplay.log')
            self.file_handler.setLevel(log_level)

            self.stdout_handler = logging.StreamHandler(sys.stdout)
            self.stdout_handler.setLevel(log_level)

            intermediate = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
            self.formatter = logging.Formatter(intermediate)

            self.file_handler.setFormatter(self.formatter)
            self.stdout_handler.setFormatter(self.formatter)

            self.logger.addHandler(self.file_handler)
            self.logger.addHandler(self.stdout_handler)
    output = Track()
    return output