from django.db import models

class GalleryImage(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField()
    image = models.ImageField(upload_to="gallery_images")
    blur_image = models.ImageField(upload_to="gallery_images")
