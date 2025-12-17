from django.contrib import admin
from .models import Event, Volunteer, EventImage
from django.utils.html import format_html
import csv
from django.http import HttpResponse

# --- Action Personnalisée : Exporter en CSV ---
def export_volunteers_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="liste_salongo.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Téléphone', 'Rôle', 'Événement', 'Statut'])
    for volunteer in queryset:
        writer.writerow([volunteer.full_name, volunteer.phone, volunteer.role, volunteer.event.title, volunteer.status])
    return response

export_volunteers_csv.short_description = "Exporter la liste sélectionnée en CSV"

# --- Configuration des Bénévoles ---
@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_display', 'role_badge', 'event_link', 'status_icon', 'status')
    list_filter = ('event__location', 'role', 'status', 'event__date') # Filtrer par Commune/Lieu [cite: 20]
    search_fields = ('full_name', 'phone', 'email')
    actions = [export_volunteers_csv]
    list_editable = ('status',) # Permet de changer le statut (Présent/Confirmé) directement depuis la liste

    # Affichage coloré pour le Rôle (Eco-brigade vs Participant)
    def role_badge(self, obj):
        colors = {
            'PARTICIPANT': 'gray',
            'LEADER': 'blue',     # Bleu PNAC
            'ECO_BRIGADE': 'green' # Vert PNAC
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 12px;">{}</span>',
            colors.get(obj.role, 'gray'),
            obj.get_role_display()
        )
    role_badge.short_description = "Rôle"

    # Lien direct vers l'événement
    def event_link(self, obj):
        return obj.event.title
    event_link.short_description = "Campagne / Salongo"

    # Formatage téléphone
    def phone_display(self, obj):
        return format_html('<b style="color: #333;">{}</b>', obj.phone)
    phone_display.short_description = "Contact"

    # Icône de statut
    def status_icon(self, obj):
        icons = {
            'PENDING': '⏳',
            'CONFIRMED': '📩',
            'PRESENT': '✅',
        }
        return icons.get(obj.status, '')
    status_icon.short_description = "État"

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3 # Affiche 3 champs vides par défaut pour uploader rapidement
    fields = ('image', 'caption')

# --- Configuration des Événements ---
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'participant_count', 'is_active')
    list_filter = ('event_type', 'is_active')
    search_fields = ('title', 'location')
    inlines = [EventImageInline]

    def participant_count(self, obj):
        count = obj.volunteers.count()
        return format_html('<b style="color: #059669;">{} inscrits</b>', count)
    participant_count.short_description = "Mobilisation"