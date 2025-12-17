from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from .models import Seminar, SeminarRegistration

def seminar_list(request):
    seminars = Seminar.objects.filter(is_active=True).order_by('start_date')
    return render(request, 'seminars/list.html', {'seminars': seminars})

def seminar_detail(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        org = request.POST.get('organization')
        p_type = request.POST.get('participant_type')
        origin = request.POST.get('origin')
        
        needs_acc = request.POST.get('needs_accommodation') == 'on'
        nights = int(request.POST.get('nights', 0)) if needs_acc else 0

        # Création de l'enregistrement (Le calcul du prix se fait dans le save() du modèle)
        registration = SeminarRegistration.objects.create(
            seminar=seminar,
            full_name=full_name,
            email=email,
            phone=phone,
            organization=org,
            participant_type=p_type,
            origin=origin,
            needs_accommodation=needs_acc,
            accommodation_nights=nights
        )

        # Préparation des données MaxiCash
        payment_context = {
            'merchant_id': settings.MAXICASH_MERCHANT_ID,
            'merchant_password': settings.MAXICASH_MERCHANT_PASSWORD,
            'amount': int(registration.total_amount * 100), # En centimes
            'currency': 'USD',
            'reference': str(registration.reference),
            'accept_url': request.build_absolute_uri('/seminars/success/'),
            'cancel_url': request.build_absolute_uri('/seminars/cancel/'),
            'decline_url': request.build_absolute_uri('/seminars/cancel/'),
            'notify_url': request.build_absolute_uri('/seminars/ipn/'),
            'gateway_url': settings.MAXICASH_GATEWAY_URL,
        }
        
        # Redirection vers la page tampon de paiement
        return render(request, 'donations/redirect_maxicash.html', payment_context)

    return render(request, 'seminars/detail.html', {'seminar': seminar})