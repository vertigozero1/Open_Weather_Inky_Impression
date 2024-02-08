import sys                  # for error handling
from PIL import Image       # for working with images
from inky.auto import auto  # for working with the e-ink display
import traceback            # for error handling

def render_image(out):
    """ Render image using inky auto """

    try:
        out.logger.debug("Rendering image to inky")
        inky = auto(ask_user=True, verbose=True)
        saturation = 0.5

        image = Image.open('weather.jpg')
        resizedimage = image.resize(inky.resolution)

        if len(sys.argv) > 2:
            saturation = float(sys.argv[2])

        inky.set_image(resizedimage, saturation=saturation)
        inky.show()
    except Exception:
        out.logger.critical("Error rendering image to inky")
        out.logger.critical(traceback.format_exc())
        sys.exit