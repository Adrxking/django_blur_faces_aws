# Generated by Django 4.1.4 on 2023-02-02 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='blur_image',
            field=models.ImageField(default='', upload_to='gallery_images'),
            preserve_default=False,
        ),
    ]
