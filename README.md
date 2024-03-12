# openWeatherInkyImpression73

## Hardware
- Raspberry Pi / power supply
  - At time of writing, the Inky Impression libraries aren't compatible with the Pi5 (which is overkill, anyway)
- [Pimoroni Inky Impression 7.3"](https://shop.pimoroni.com/products/inky-impression-7-3?variant=40512683376723)
- MicroSD card -- no special requirements
- A case/mount/frame for display

## Deployment
### Preparation
- Format the card
  - Recommend the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/) utility, and the 64 bit Raspbian Lite image
- Boot the Pi and wait for the activity light to stop blinking
- SSH into it using the credentials configured during imaging
- `sudo raspi-config` and enable I2C and SPI
- `sudo apt update && sudo apt upgrade -y` for good measure
- `sudo apt install python3-pip` to install pip3
- 
