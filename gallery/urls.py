from gallery.views import gallery_view
from django.urls import path

urlpatterns = [
    # ... autres urls
    path('galerie/', gallery_view, name='gallery'),
]