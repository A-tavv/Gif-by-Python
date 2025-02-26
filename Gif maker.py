import os
import imageio.v3 as iio
from PIL import Image, ExifTags
import numpy as np

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the images folder
image_folder = os.path.join(current_dir, "images")

# Define the input file paths
filenames = [
    os.path.join(image_folder, "image1.JPG"),
    os.path.join(image_folder, "image2.JPG"),
    os.path.join(image_folder, "image3.JPG")
]

# Initialize the list for storing images
images = []

# Target size for the square frame
target_size = (1000, 1000)

def fit_image_to_square(image, target_size):
    """
    Resizes and pads an image to fit into a square frame while preserving its original orientation.
    """
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation)
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass  # No EXIF data

    img = image.convert("RGB")  # Ensure RGB mode
    width, height = img.size
    aspect_ratio = width / height

    if aspect_ratio < 1:
        new_height = target_size[1]
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = target_size[0]
        new_height = int(new_width / aspect_ratio)

    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    new_img = Image.new("RGB", target_size, (0, 0, 0))  # Black background
    x_offset = (target_size[0] - new_width) // 2
    y_offset = (target_size[1] - new_height) // 2
    new_img.paste(img_resized, (x_offset, y_offset))

    return new_img

# Process all images
for filename in filenames:
    if os.path.exists(filename):  # Check if file exists
        img = Image.open(filename)
        img_fitted = fit_image_to_square(img, target_size)
        images.append(np.array(img_fitted))  # Convert to numpy array
    else:
        print(f"⚠️ Warning: File not found - {filename}")

# the output file path
output_path = os.path.join(current_dir, "output.gif")

# Write the images as a GIF only if images exist
if images:
    iio.imwrite(output_path, images, duration=100, loop=0)
    print(f"✅ GIF saved at: {output_path}")
else:
    print("❌ No images found, GIF not created.")
