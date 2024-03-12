# openWeatherInkyImpression73

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
  - `source ~/.virtualenvs/pimoroni/bin/activate`
- **ALTERNATELY** you can just use [an older distro](http://downloads.raspberrypi.org/raspios_oldstable_arm64/images/raspios_oldstable_arm64-2023-10-10/2023-05-03-raspios-bullseye-arm64.img.xz)
- `pip3 install inky[rpi,example-depends]`
### Software Preparation
- `sudo apt install git`
- 
