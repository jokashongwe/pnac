from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import des vues
from core.views import home, mission
from events.views import event_list, join_event, event_detail, event_map_data
from donations.views import donate
from team.views import team_page

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core
    path('', home, name='home'),
    path('notre-mission/', mission, name='mission'),
    
    # Événements
    path('events/', event_list, name='event_list'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/join/<int:event_id>/', join_event, name='join_event'),
    path('api/map-data/', event_map_data, name='event_map_data'),
    
    # Dons
    path('donate/', donate, name='donate'),

    # Team
    path('equipe/', team_page, name='team'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)