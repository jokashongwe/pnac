from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Volunteer

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'events/index.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

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