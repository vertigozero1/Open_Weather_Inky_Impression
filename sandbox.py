from inky.auto import auto                  # for working with the e-ink display
from PIL import Image,ImageDraw,ImageFont   # for rendering via PIL

""" Render text to image using PIL """
""" Urbanist-Thin.ttf,          Urbanist-ThinItalic.ttf
    Urbanist-ExtraLight.ttf,    Urbanist-ExtraLightItalic.ttf
    Urbanist-Light.ttf,         Urbanist-LightItalic.ttf
    Urbanist-Regular.ttf,       Urbanist-Italic.ttf
    Urbanist-Medium.ttf,        Urbanist-MediumItalic.ttf
    Urbanist-SemiBold.ttf,      Urbanist-SemiBoldItalic.ttf
    Urbanist-Bold.ttf,          Urbanist-BoldItalic.ttf
    Urbanist-ExtraBold.ttf,     Urbanist-ExtraBoldItalic.ttf
    Urbanist-Black.ttf,         Urbanist-BlackItalic.ttf
"""

y_position = 0
max_width = 800
max_height = 480
canvas = Image.new('RGB', (max_width, max_height), "white")
draw = ImageDraw.Draw(canvas)

paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Thin.ttf", 10, encoding="unic")

dummy_width, paragraph_height = paragraph.getsize("Ag")
x_position = max_width / 2
y_position = paragraph_height
while y_position < max_height - paragraph_height:
    draw.text((x_position, y_position), str(y_position), 'black', paragraph)
    y_position += paragraph_height

# save the blank canvas to a file
canvas.save("pil-text.png", "PNG")

inky = auto(ask_user=True, verbose=True)
saturation = 0.5

image = Image.open("pil-text.png")
resizedimage = image.resize(inky.resolution)

inky.set_image(resizedimage, saturation=saturation)
canvas.show()
inky.show()