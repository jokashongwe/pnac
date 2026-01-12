from django.urls import path
from .views import forum_index, topic_detail

urlpatterns = [
    path('', forum_index, name='forum_index'),
    path('sujet/<slug:slug>/', topic_detail, name='topic_detail'),
]