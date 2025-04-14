from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ProcessedImage
from .image_processing import apply_filter_chain
from django.conf import settings
import os
import boto3


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save original first
                image = form.save()

                # Process with all selected filters
                processed_path = apply_filter_chain(
                    image.original_image.path,
                    form.cleaned_data['filters']
                )

                # Save processed reference
                image.processed_image.name = os.path.relpath(processed_path, settings.MEDIA_ROOT)
                image.save()
                s3 = boto3.client('s3', region_name=settings.AWS_REGION_NAME)
                original_image_path = image.original_image.path
                original_s3_key = f"original/{os.path.basename(original_image_path)}"
                s3.upload_file(original_image_path, settings.AWS_STORAGE_BUCKET_NAME, original_s3_key)

                return redirect('display_image', pk=image.pk)

            except Exception as e:
                if 'image' in locals():
                    image.delete()
                return render(request, 'upload.html', {
                    'form': form,
                    'error': f"Processing failed: {str(e)}"
                })

    form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def display_image(request, pk):
    try:
        image = ProcessedImage.objects.get(pk=pk)
        return render(request, 'display.html', {'image': image})
    except ProcessedImage.DoesNotExist:
        return render(request, 'upload.html', {'error': 'Image not found'})
