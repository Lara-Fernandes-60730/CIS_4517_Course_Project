from PIL import Image, ImageFilter, ImageOps
import os

def apply_filter(original_image_path, filter_type):
    '''
    Applies selected filter to the image
    image_path: Path to original_image
    filter_type: Which filter to apply to the photo

    Returns path to processed image
    '''

    img = Image.open(original_image_path)

    #Apply filters
    if filter_type == 'gray':
        processed_img = img.convert('L')

    elif filter_type == 'sepia':
        processed_img = apply_sepia(img)

    elif filter_type == 'poster':
        processed_img = ImageOps.posterize(img, 3)

    elif filter_type == 'blur':
        processed_img = img.filter(ImageFilter.BLUR)

    elif filter_type == 'edge':
        processed_img = img.filter(ImageFilter.FIND_EDGES)

    elif filter_type == 'solar':
        processed_img = ImageOps.solarize(img, threshold=128)

    #Save processed image
    base_path, ext = os.path.splittext(original_image_path)
    processed_path = f"{base_path}_{filter_type}{ext}"
    processed_img.save(processed_path)

    return processed_path

def apply_sepia(img):
    '''
    Custom sepia filter implementation
    img: PIL Image object
    Returns processed PIL Image object
    '''

    width, height = img.size

    # Create editable copy of image
    pixels = img.load()

    # Process each pixel
    for py in range(height):
        for px in range(width):
            # Get original RGB values
            r, g, b = img.getpixel((px, py))

            # Calculate sepia value
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255

            pixels[px,py] = (tr, tg, tb)

    return img