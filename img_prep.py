import random
from PIL import Image

def load_image(filename):
    try:
        image = Image.open(filename)
        return image
    except IOError:
        print("Unable to load image")
        return None

def save_image(image, filename):
    try:
        image.save(filename)
    except IOError:
        print("Unable to save image")

def select_columns(image, column_width_range, selection_percentage):
    width, height = image.size
    min_column_width, max_column_width = column_width_range

    # Calculate the total number of selected pixels
    total_pixels = int((height - 40) * (width * selection_percentage))

    selected_columns = []
    selected_pixels = 0

    while selected_pixels < total_pixels:
        column_width = random.randint(min_column_width, max_column_width)
        column_start = random.randint(20, width - column_width - 20)
        column_end = column_start + column_width

        selected_columns.append((column_start, column_end))
        selected_pixels += column_width * (height - 40)

    return selected_columns

def fill_distorted_image(input_image, selected_columns):
    width, height = input_image.size
    distorted_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            if x >= 20 and x < width - 20:
                for column_start, column_end in selected_columns:
                    if x >= column_start and x < column_end:
                        # Calculate the midpoint of the selected column
                        midpoint = (column_start + column_end) // 2

                        # Calculate the amount of pixels to fill from each side
                        left_pixels = x - column_start
                        right_pixels = column_end - x

                        # Calculate the weight for left and right pixels using a Gaussian distribution
                        weight_left = random.gauss(0.5, 0.1)
                        weight_right = 1 - weight_left

                        # Calculate the new pixel value based on the weights
                        pixel_left = input_image.getpixel((midpoint - left_pixels, y))
                        pixel_right = input_image.getpixel((midpoint + right_pixels, y))

                        new_pixel = (
                            int(pixel_left[0] * weight_left + pixel_right[0] * weight_right),
                            int(pixel_left[1] * weight_left + pixel_right[1] * weight_right),
                            int(pixel_left[2] * weight_left + pixel_right[2] * weight_right)
                        )

                        distorted_image.putpixel((x, y), new_pixel)
                        break
                else:
                    distorted_image.putpixel((x, y), input_image.getpixel((x, y)))
            else:
                distorted_image.putpixel((x, y), input_image.getpixel((x, y)))

    return distorted_image

# Define the parameters
input_filename = "data_ex.ppm"
output_filename = "distorted.ppm"
column_width_range = (8, 30)
selection_percentage = 0.20

# Load the input image
input_image = load_image(input_filename)
if input_image is None:
    exit()

# Select the columns
selected_columns = select_columns(input_image, column_width_range, selection_percentage)

# Fill the distorted image
distorted_image = fill_distorted_image(input_image, selected_columns)

# Copy the original pixels within the outer 40 pixels
for x in range(20):
    for y in range(input_image.height):
        distorted_image.putpixel((x, y), input_image.getpixel((x, y)))

for x in range(input_image.width - 20, input_image.width):
    for y in range(input_image.height):
        distorted_image.putpixel((x, y), input_image.getpixel((x, y)))

# Save the distorted image
save_image(distorted_image, output_filename)
