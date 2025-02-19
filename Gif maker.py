import imageio.v3 as iio
from PIL import Image, ImageOps, ExifTags
import numpy as np

# Define the input file paths
filenames = #[File_path]

# Initialize the list for storing images
images = []

# Target size for the square frame
target_size = (1000, 1000)

def fit_image_to_square(image, target_size):
    """
    Resizes and pads an image to fit into a square frame while preserving its original orientation.
    """
    # Correct the orientation based on EXIF data if available
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
        # No EXIF data or no orientation tag, proceed as-is
        pass

    img = image.convert("RGB")  # Ensure the image is in RGB mode

    # Determine the aspect ratio of the image
    width, height = img.size
    aspect_ratio = width / height

    # If the image is vertical (height > width)
    if aspect_ratio < 1:
        new_height = target_size[1]
        new_width = int(new_height * aspect_ratio)
    else:
        # If the image is horizontal or square (width >= height)
        new_width = target_size[0]
        new_height = int(new_width / aspect_ratio)

    # Resize the image while maintaining aspect ratio
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a square canvas
    new_img = Image.new("RGB", target_size, (0, 0, 0))  # Black background
    # Calculate position to center the image
    x_offset = (target_size[0] - new_width) // 2
    y_offset = (target_size[1] - new_height) // 2
    new_img.paste(img_resized, (x_offset, y_offset))
    return new_img

# Process all images
for filename in filenames:
    img = Image.open(filename)
    img_fitted = fit_image_to_square(img, target_size)
    images.append(np.array(img_fitted))  # Convert to numpy array

# Define the output file path
output_path = "D:\\output.gif"

# Write the images as a GIF
iio.imwrite(output_path, images, duration=100, loop=0)
