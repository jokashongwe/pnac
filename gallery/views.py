from django.shortcuts import render
from .models import GalleryImage

def gallery_view(request):
    images = GalleryImage.objects.all()
    categories = GalleryImage.CATEGORY_CHOICES
    return render(request, 'gallery/index.html', {'images': images, 'categories': categories})