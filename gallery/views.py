import json
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import cv2
import boto3
from django.shortcuts import render, redirect
from .models import GalleryImage
from .forms import GalleryImageForm, DeleteAllImages
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.db.models.fields.files import ImageFieldFile
import os

def gallery_view(request):
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    if request.method == "PUT":
        image_info = json.loads(request.body)
        print(image_info)
        image = Image.open('./gallery_images/johnny_3OfKQ4U.jpg')
        width, height = image.size
        new_width = int(width * 300 / height)
        resized_image = image.resize((new_width, 300))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.20,
            minNeighbors = 6,
            minSize = (30, 30)
        )
        print("Found {0} Faces!".format(len(faces)))
        print(faces)

        # resized_image.save("path/to/resized_image.jpg")
        print(image)
        print(resized_image)

    form = GalleryImageForm()
    images = GalleryImage.objects.all()
    return render(request, "gallery.html", {"images": images, "form": form})

def remove_all(request):
    if request.method == "POST":
        # Handle "remove all" form submission
        remove_images_form = DeleteAllImages(request.POST)
        if remove_images_form.is_valid():
            # Delete all images
            GalleryImage.objects.all().delete()
            return redirect("/")

    # Create forms for rendering in the template
    remove_images_form = DeleteAllImages()
    return render(request, "remove_all_images.html", {"removeAll": remove_images_form})

def detect_faces(request, image_id):
    info = GalleryImage.objects.get(id = image_id)
    session = boto3.Session(region_name='us-west-2')
    rekognition = session.client('rekognition')

    with open('.' + info.image.url.replace('/media', ''), 'rb') as image_file:
        image = image_file.read()

    response = rekognition.detect_faces(Image = { 'Bytes': image }, Attributes = [ 'ALL' ])
    filtered_faces = filter(lambda face: face["AgeRange"]["Low"] < 18, response['FaceDetails'])
    filtered_faces = list(map(lambda face: face['BoundingBox'], filtered_faces))
    return JsonResponse(filtered_faces, safe = False)

def usaajax(request):
    return render(request, 'usaajax.html')

def get_single_image(request, id):   
    image = GalleryImage.objects.get(id = id)
    csrf_token = get_token(request)
    return render(request, 'single_image.html', {'image': image, 'csrf_token': csrf_token})

def get_all_images(request):
    images = GalleryImage.objects.all()
    return render(request, 'all_images.html', {'images': images})

def blur_image(request, id):
    image = GalleryImage.objects.get(id = id)

    path = image.image.url
    path = path.replace('/media', '.')

    img = Image.open(path)
    body = json.loads(request.body)

    coords = body.get('coords')
    for coord in coords:
        x = int(coord['x'])
        y = int(coord['y'])
        w = int(coord['w'])
        h = int(coord['h'])
        region = img.crop((x, y, x + w, y + h))
        for i in range(0, 40):
            region = region.filter(ImageFilter.BLUR)
        img.paste(region, (x, y, x + w, y + h))
    extension = os.path.splitext(path)[1]
    extension_length = len(extension)
    path = path[:-extension_length] + "-blured" + path[-extension_length:]
    img.save(path)
    
    image.blur_image = ImageFieldFile(image, image.blur_image, path)
    image.save()

    return JsonResponse({})
    
    
def apply_blur(image_path, coords):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    for coord in coords:
        x, y, w, h = coord["x"], coord["y"], coord["w"], coord["h"]
        draw.rectangle([x, y, x+w, y+h], fill=(255, 255, 255))
    img.save(image_path)

    