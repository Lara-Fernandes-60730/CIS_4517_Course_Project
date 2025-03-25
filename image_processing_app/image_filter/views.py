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
            original_image = form.save()

            #Get selected filters from the form
            filter_list = form.cleaned_data['filter_list']

            #Apply filters and return path to the processed image
            processed_image_path = apply_filter(original_image.original_image.path, filter_list)

            #Save the image and make absolute path relative for storage
            rel_path = os.path.relpath(processed_image_path, settings.MEDIA_ROOT)

            original_image.processed_image = rel_path
            original_image.filter_list = filter_list
            original_image.save()

            return redirect('display_image', pk=original_image.pk)

        else:
            # if GET request fails
            form = ImageUploadForm()

        return render(request, 'upload.html', {'form': form})

    def display_image(request, pk):
        '''
        Shows the processed image with filters now applied
        pk: Primary key of image to be displayed
        '''
        image = ProcessedImage.objects.get(pk=pk)

        return render(request, 'display.html', {'image': image})