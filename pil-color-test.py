from inky.auto import auto
from PIL import Image,ImageDraw,ImageFont,ImageColor


# Define the size of the image
image_width = 800
image_height = 480

# Create a new image with a white background
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# Define the font and font size
font_size = 10
font = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Thin.ttf", font_size)

# Get a list of all PIL colors
colors = list(ImageColor.colormap.keys())

# Calculate the number of columns and rows
num_columns = 10
num_rows = len(colors) // num_columns + 1

# Draw examples of each color with their names
for i, color in enumerate(colors):
    column = i % num_columns
    row = i // num_columns

    # Calculate the position of the color example
    x = column * (image_width // num_columns)
    y = row * (image_height // num_rows)

    # Draw a rectangle with the color
    draw.rectangle([(x, y), (x + image_width // num_columns, y + image_height // num_rows)], fill=color)

    # Draw the color name
    draw.text((x, y), color, font=font, fill="black")

# Save the image
image.save("color_examples.png")

inky = auto(ask_user=True, verbose=True)
saturation = 1

inky.set_image(image, saturation=saturation)
image.show()
inky.show()