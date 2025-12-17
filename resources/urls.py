from resources.views import resource_list
from django.urls import path

urlpatterns = [
    # ... autres urls
    path('ressources/', resource_list, name='resource_list'),
]