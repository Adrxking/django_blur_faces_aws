from django import forms
from .models import GalleryImage

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["title", "image"]
        
class DeleteAllImages(forms.Form):
    submit = forms.BooleanField(label="Delete All Rows", initial=False, required=False)
