from django.db import models
from django.urls import reverse

class ProcessedImage(models.Model):
    # Use consistent naming (filter_list → filters_applied)
    FILTER_CHOICES = [
        ('gray', 'Grayscale'),
        ('sepia', 'Sepia'),
        ('poster', 'Poster'),
        ('blur', 'Blur'),
        ('edge', 'Edge Detection'),
        ('solar', 'Solarize'),
    ]

    original_image = models.ImageField(
        upload_to='original/%Y/%m/%d/',
        verbose_name="Original Image"
    )

    processed_image = models.ImageField(
        upload_to='processed/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name="Processed Image"
    )

    filters_applied = models.CharField(
        max_length=255,
        verbose_name="Applied Filters"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creation Date"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Processed Image"
        verbose_name_plural = "Processed Images"

    def __str__(self):
        return f"Image #{self.id} with {self.filters_applied}"

    def get_absolute_url(self):
        return reverse('display_image', kwargs={'pk': self.pk})

    @property
    def filters_list(self):
        """Returns filters as a list"""
        return self.filters_applied.split(',') if self.filters_applied else []
