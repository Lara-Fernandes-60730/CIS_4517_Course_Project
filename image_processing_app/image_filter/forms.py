from django import forms
from .models import ProcessedImage

#Define filters
FILTER_OPTIONS = [
    ('gray', 'Grayscale'), # Converts to black and white
    ('sepia', 'Sepia'),    # Applies sepia tone
    ('poster', 'Poster'),  # Reduces number of colors
    ('blur', 'Blur'),      # Applies blue effect
    ('edge', 'Edge Detection'), # Highlights edges
    ('solar', 'Solarize')   # Inverse colors above threshold
]

class ImageUploadForm(forms.ModelForm):
    '''
    Form for uploading image and selecting filters.
    Automatically created from the ProcessedImage model
    '''

    # Choice field allows users to select filters
    filters = forms.MultipleChoiceField(
        choices=ProcessedImage.FILTER_CHOICES,  # Reference from model
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Filters"
    )

    class Meta:
        # Specifies which model the form is based on
        model = ProcessedImage

        #Only include fields from the above model
        fields = ['original_image']
