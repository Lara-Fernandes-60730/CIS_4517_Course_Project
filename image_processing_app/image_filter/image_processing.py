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
    processed_path = f"{base_path}_processed{ext}"
    processed_img.save(processed_path)

    return processed_path

def apply_sepia(img):
    return " "