from django.urls import path
from . import views

#Maps URLS to view functions

urlpatterns = [
    # Empty path ('') maps to upload_image view
    path('', views.upload_image, name='upload_image'),

    # Path such as 'display/1/' maps to display_image view oth pk = 1
    path('display/<int:pk>/', views.display_image, name='display_image'),
]