from django.urls import path

from .views import delete_post, forum_index, request_topic_access, topic_detail

urlpatterns = [
    path("", forum_index, name="forum_index"),
    path("sujet/<slug:slug>/", topic_detail, name="topic_detail"),
    path("sujet/<slug:slug>/demander-acces/", request_topic_access, name="request_topic_access"),
    path("posts/<int:post_id>/supprimer/", delete_post, name="delete_post"),
]
