from PIL import Image, ImageFilter, ImageOps
import os
import uuid
from datetime import datetime
from django.conf import settings
import boto3


def generate_output_path(original_path):
    """Generates clean output paths with UUID only"""
    original_name = os.path.basename(original_path)
    base, ext = os.path.splitext(original_name)
    unique_id = uuid.uuid4().hex[:6]  # 6-char ID

    processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    return os.path.join(processed_dir, f"{base}_{unique_id}{ext}")

def apply_filter_chain(original_path, filter_types):
    """
    Applies all selected filters to a PIL Image object and returns the modified image
    img: The image to process
    filter_types: The filters to apply

    Returns processed image
    """
    img = Image.open(original_path)

    # Determine processing order
    processing_order = []
    if 'gray' in filter_types:
        processing_order.append('gray')
    if 'sepia' in filter_types:
        processing_order.append('sepia')
    # Add other filters (excluding gray/sepia)
    processing_order.extend([f for f in filter_types if f not in ['gray', 'sepia']])

    # Apply filters in determined order
    for filter_type in processing_order:
        img = apply_filter(img, filter_type)

    output_path = generate_output_path(original_path)
    img.save(output_path)

    s3 = boto3.client('s3', region_name=settings.AWS_REGION_NAME)
    processed_s3_key = f"processed/{os.path.basename(output_path)}"
    s3.upload_file(output_path, settings.AWS_STORAGE_BUCKET_NAME, processed_s3_key)

    return output_path


def apply_filter(img, filter_type):
    """
    Applies a single filter to a PIL Image object and returns the modified image
    img: The image to process
    filter_type: Which filter to apply

    Returns processed image
    """
    try:
        if filter_type == 'gray':
            return img.convert('L')
        elif filter_type == 'sepia':
            return apply_sepia(img)
        elif filter_type == 'poster':
            return ImageOps.posterize(img, 3)
        elif filter_type == 'blur':
            return img.filter(ImageFilter.GaussianBlur(radius=3))
        elif filter_type == 'edge':
            return img.filter(ImageFilter.FIND_EDGES)
        elif filter_type == 'solar':
            return ImageOps.solarize(img, threshold=128)
        else:
            return img  # Return unchanged if filter not recognized
    except Exception as e:
        print(f"Error applying filter {filter_type}: {str(e)}")
        return img  # Fallback to original image on error

def apply_sepia(img):
    '''
    Custom sepia filter implementation
    img: PIL Image object
    Returns processed PIL Image object
    '''

    if img.mode == 'L':  # Grayscale image
        # Create sepia-toned grayscale
        sepia_filter = Image.new('L', img.size, 150)  # Mid-tone sepia base
        return Image.blend(img, sepia_filter, alpha=0.7)
    else:  # Color image
        width, height = img.size
        pixels = img.load()
        for py in range(height):
            for px in range(width):
                r, g, b = img.getpixel((px, py))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[px, py] = (
                    min(255, tr),
                    min(255, tg),
                    min(255, tb)
                )
        return img
