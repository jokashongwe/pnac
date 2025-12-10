from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Event, Volunteer

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'events/index.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def event_map_data(request):
    """API pour envoyer les coordonnées à la carte Leaflet"""
    events = Event.objects.filter(is_active=True, latitude__isnull=False, longitude__isnull=False)
    
    data = []
    for event in events:
        data.append({
            'title': event.title,
            'lat': event.latitude,
            'lng': event.longitude,
            'status': event.map_status,
            'url': f"/events/{event.id}/", # Lien vers le détail
            'location': event.location,
            'date': event.date.strftime('%d/%m/%Y')
        })
    
    return JsonResponse(data, safe=False)

def join_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        
        # Récupération des données du formulaire
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        is_eco_brigade = request.POST.get('is_eco_brigade') # Checkbox

        # Détermination du rôle
        role = 'ECO_BRIGADE' if is_eco_brigade else 'PARTICIPANT'

        # Création du bénévole
        Volunteer.objects.create(
            event=event,
            full_name=full_name,
            phone=phone,
            role=role,
            status='PENDING' # En attente de validation admin
        )

        # Message de succès (Vert)
        messages.success(request, f"Merci {full_name} ! Votre inscription pour '{event.title}' est enregistrée.")
        
        return redirect('event_list') # Retour à la liste
    
    return redirect('event_list')