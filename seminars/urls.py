from django.urls import path
from .views import seminar_list, seminar_detail

urlpatterns = [
    path('', seminar_list, name='seminar_list'),
    path('<int:seminar_id>/', seminar_detail, name='seminar_detail'),
    # Note: On réutilise les vues success/cancel de l'app donations ou on en crée de nouvelles
]