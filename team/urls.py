from django.urls import path
from .views import team_page, volunteer_apply

urlpatterns = [
    path('', team_page, name='team'),
    path('rejoindre/', volunteer_apply, name='volunteer_apply'),
]
