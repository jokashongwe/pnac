from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
# Import des vues
from core.views import home, mission
from events.views import event_list, join_event, event_detail, event_map_data
from donations.views import donate
from team.views import team_page
from gallery.views import gallery_view
from resources.views import resource_list

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    
    # Core
    path('', home, name='home'),
    path('notre-mission/', mission, name='mission'),
    
    # Événements
    path('actions/', event_list, name='event_list'),
    path('actions/<int:event_id>/', event_detail, name='event_detail'),
    path('actions/join/<int:event_id>/', join_event, name='join_event'),
    path('api/map-data/', event_map_data, name='event_map_data'),
    
    # Dons
    path('donate/', donate, name='donate'),

    path('gallery', gallery_view, name='gallery'),
    path('resources/', resource_list, name='resource_list'),
    # Team
    path('equipe/', team_page, name='team'),
    path('actualites/', include('blog.urls')),
    path('forum/', include('forum.urls')),

)