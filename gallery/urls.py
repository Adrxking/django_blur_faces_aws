from django.urls import path
from .views import gallery_view, remove_all, detect_faces, usaajax, get_single_image, get_all_images, blur_image

urlpatterns = [
    path("", gallery_view, name="gallery"),
    path("amazon_face/<int:image_id>", detect_faces, name="detect_faces"),
    path("usaajax/", usaajax, name="usaajax"),
    path("remove/", remove_all, name="remove"),
    path("single_image/<int:id>", get_single_image, name="single_image"),
    path("all_images/", get_all_images, name="all_images"),
    path("blur_image/<int:id>", blur_image, name="blur_image"),
]
