from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ProcessedImage
from .image_processing import apply_filter
import os
from django.conf import settings

def upload_image(request):
    '''
    Handles the image upload page
    request: Contains information about the current web request
    '''

    if request.method == 'POST':
        # If a form was submitted
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded image to database
            image = form.save(commit=False)

            #Get selected filters from the form
            selected_filters = form.cleaned_data['filter_list']

            #Save to create the ID for the image
            image.save()

            #Apply filters and return path to the processed image
            processed_image_path = image.original_image.path
            for filter_name in selected_filters:
                processed_image_path = apply_filter(processed_image_path, filter_name)

            #Save image
            relative_path = os.path.relpath(processed_image_path, settings.MEDIA_ROOT)
            image.processed_image = relative_path
            image.save()

            return redirect('display_image', pk=image.pk)

        else:
            # if GET request fails
            form = ImageUploadForm()

        return render(request, 'upload.html', {'form': form})

def display_image(request, pk):
    '''
    Shows the processed image with filters now applied
    pk: Primary key of image to be displayed
    '''
    try:
        image = ProcessedImage.objects.get(pk=pk)
        if not image.processed_image:
            raise ValueError("No processed image available")
        return render(request, 'display.html', {'image': image})


    except(ProcessedImage.DoesNotExist, ValueError) as e:
        return render(request, 'error.html', {'error': str(e)})