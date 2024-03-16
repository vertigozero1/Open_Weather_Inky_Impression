# Open_Weather_Inky_Impression
## An open-source weather display for two cities' current conditions and seven-day forecast, running on a rasPi and e-ink multi-color display, using OpenWeatherMap's API

### Notes
- ***Most modern RasPi hardware is over-powered for this application, which leaves it free to serve other purposes (Home Assistant, PiHole, file server, etc.).***
- ***The e-ink screen I've chosen for this is a 7.3" seven-color display which takes ~40 seconds to refresh; this is fine for this use case, since this updates hourly.***
  - ***If you want this to serve double-duty as a clock, you'll need to swap the screen and modify the code to fit the size, resolution, and colors of the new one. It may also require extensive refactoring to replace the Inky library if you pick a different manufacturer.***

||
# work in progress - current main branch works decently but may have minor glitches or aesthetic quirks/fork is a major revision in the works
||

## Hardware
- Raspberry Pi / power supply
  - At time of writing, the Inky Impression libraries aren't compatible with the Pi5 (which is overkill, anyway)
- [Pimoroni Inky Impression 7.3"](https://shop.pimoroni.com/products/inky-impression-7-3?variant=40512683376723)
- MicroSD card -- no special requirements
- A case/mount/frame for display

## Deployment
### Hardware Preparation
- Format the card
  - Recommend the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/) utility, and the 64 bit Raspbian Lite image
- Mount the Pi to the screen, and 
- Boot the Pi and wait for the activity light to stop blinking
- SSH into it using the credentials configured during imaging
- `sudo raspi-config` and enable I2C and SPI
- `sudo apt update && sudo apt upgrade -y` for good measure
- `sudo apt install python3-pip` to install pip3
- At this point, if you're running a modern version of PiOS, [you're going to need a Python virtual environment (or possibly break things down the line)](https://github.com/pimoroni/boilerplate-python/pull/13)
  - `mkdir ~/.virtualenvs`
  - `mkdir ~/.virtualenvs/pimoroni`
  - `python3 -m venv --system-site-packages ~/.virtualenvs/pimoroni/`
  - `sudo nano ~/.bashrc`
    - paste the following into the bottom of the file
    - ```
      # Generate python venv for Pimoroni Impression
      # https://github.com/pimoroni/boilerplate-python/pull/13
      PY_ENV_DIR=$HOME/.virtualenvs/pimoroni
      if [ ! -f $PY_ENV_DIR/bin/activate ]; then
        printf "Creating user Python environment in $PY_ENV_DIR, please wait...\n"
        mkdir -p $PY_ENV_DIR
        python3 -m venv --system-site-packages $PY_ENV_DIR
      fi
      printf " ↓ ↓ ↓ ↓   Hello, we've activated a Python venv for you. To exit, type \"deactivate\".\n"
      source $PY_ENV_DIR/bin/activate
      ```
  - `source ~/.virtualenvs/pimoroni/bin/activate`
- **ALTERNATELY** you can just use [an older distro](http://downloads.raspberrypi.org/raspios_oldstable_arm64/images/raspios_oldstable_arm64-2023-10-10/2023-05-03-raspios-bullseye-arm64.img.xz)
### Software Dependencies
- register for an API key, using https://openweathermap.org/api
- install urbanist font https://github.com/coreyhu/Urbanist/
-   ```
    curl -L -O https://github.com/coreyhu/Urbanist/releases/download/1.330/Urbanist-fonts.zip
    unzip Urbanist-fonts.zip
    cd Urbanist-fonts/fonts/ttf/
    sudo cp *.* /usr/share/fonts/truetype
    cd ~/
    ```
- `pip3 install inky[rpi,example-depends]` https://github.com/pimoroni/inky
- `pip3 install scikit-learn` https://scikit-learn.org/stable/install.html
- `pip3 install pillow` https://pillow.readthedocs.io/en/latest/installation.html
### Software Preparation
- `sudo apt install git`
- `git clone https://github.com/vertigozero1/Open_Weather_Inky_Impression.git`
- `cp config.ini.DEFAULT config.ini`
- `sudo nano config.ini`
  - replace the values with the appropriate data
### Initial Test
- `python weather_display.py`
### Scheduling
- `crontab-e`
- add the below to the bottom of the file
- ```
  # Run the weather display application under the python virtual environment
  @reboot $HOME/.virtualenvs/pimoroni/bin/python ~/Open_Weather_Inky_Impression/weather_display.py
  @hourly $HOME/.virtualenvs/pimoroni/bin/python ~/Open_Weather_Inky_Impression/weather_display.py
  ```
  - If you opted to avoid the Python virtual environment, replace the above lines with `python weather_display.py` after @reboot and @hourly, respectively
