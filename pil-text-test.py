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

big_number = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Black.ttf", 64, encoding="unic")
mid_number = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Bold.ttf", 21, encoding="unic")

def get_color(temp):
    if temp <= 39:
        color = 'powderblue'
        outline_color = 'darkturquoise'
    elif 40 <= temp <= 49:
        color = 'lightblue'
        outline_color = 'darkturquoise'
    elif 50 <= temp <= 59:
        color = 'lightskyblue'
        outline_color = 'darkturquoise'
    elif 60 <= temp <= 69:
        color = 'cornflowerblue'
        outline_color = 'darkturquoise'
    elif 70 <= temp <= 79:
        color = 'goldenrod'
        outline_color = 'black'
    elif 80 <= temp <= 89:
        color = 'lightcoral'
        outline_color = 'maroon'
    elif 90 <= temp <= 99:
        color = 'hotpink'
        outline_color = 'maroon'
    elif 100 <= temp <= 109:
        color = 'firebrick'
        outline_color = 'maroon'
    elif 110 <= temp:
        color = 'floralwhite'
        outline_color = 'firebrick'
    else:
        color = 'black'
        outline_color = 'black'
    return color, outline_color

x_position = 20
y_position = 20
column_width = 100
temp_list = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
for temp in temp_list:
    if temp == 80:
        y_position = 20
        x_position += (column_width * 2)
    text_color, text_outline_color = get_color(temp)

    position = (x_position, y_position)

    draw.text(position, f"{temp}", text_color, big_number, stroke_width=2, stroke_fill=text_outline_color)

    temp_x_position = x_position + column_width
    position = (temp_x_position, y_position)

    draw.text(position, f"{temp}", text_color, mid_number, stroke_width=1, stroke_fill=text_outline_color)
    y_position += 60

# save the blank canvas to a file
canvas.save("pil-text.png", "PNG")

inky = auto(ask_user=True, verbose=True)
saturation = 0.5

image = Image.open("pil-text.png")
resizedimage = image.resize(inky.resolution)

inky.set_image(resizedimage, saturation=saturation)
canvas.show()
inky.show()