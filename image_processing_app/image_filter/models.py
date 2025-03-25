from django.db import models

class ProcessedImage(models.Model):

    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)

    filter_list= models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        "String representation of model shown in the admin interface"
        return f"Image processed with filters: {self.filter_list}"
