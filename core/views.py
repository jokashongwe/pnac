from django.shortcuts import render
from django.db.models import Sum, Count
from events.models import Event, Volunteer
from donations.models import Donation

def home(request):
    # 1. Calcul des statistiques pour la section "Impact"
    total_volunteers = Volunteer.objects.count()
    
    # On calcule la somme des dons (si aucun don, on retourne 0)
    total_raised_data = Donation.objects.aggregate(Sum('amount'))
    total_raised = total_raised_data['amount__sum'] or 0
    
    # Nombre d'événements réalisés ou prévus
    total_events = Event.objects.filter(is_active=True).count()

    # 2. Récupérer les 3 prochains événements pour l'accueil
    upcoming_events = Event.objects.filter(is_active=True).order_by('date')[:3]

    context = {
        'total_volunteers': total_volunteers,
        'total_raised': round(total_raised), # Arrondi pour l'affichage
        'total_events': total_events,
        'upcoming_events': upcoming_events,
    }
    
    return render(request, 'home.html', context)