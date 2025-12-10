from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Donation

def donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name') or "Anonyme"

        # 1. Créer la donation en base de données (Statut: PENDING)
        donation = Donation.objects.create(
            amount=amount,
            email=email,
            phone=phone,
            donor_name=name
        )

        # 2. Préparer les données pour MaxiCash
        context = {
            'merchant_id': settings.MAXICASH_MERCHANT_ID,
            'merchant_password': settings.MAXICASH_MERCHANT_PASSWORD,
            'amount': int(float(amount) * 100), # MaxiCash attend souvent des centimes (vérifier doc)
            'currency': 'USD',
            'reference': str(donation.reference),
            'accept_url': request.build_absolute_uri('/donate/success/'),
            'cancel_url': request.build_absolute_uri('/donate/cancel/'),
            'decline_url': request.build_absolute_uri('/donate/cancel/'),
            'notify_url': request.build_absolute_uri('/donate/ipn/'), # Instant Payment Notification
            'gateway_url': settings.MAXICASH_GATEWAY_URL,
            'donation': donation
        }

        # 3. Afficher la page de redirection (intermédiaire)
        return render(request, 'donations/redirect_maxicash.html', context)

    return render(request, 'donate.html')

# --- Pages de retour ---

def payment_success(request):
    # Idéalement, on vérifie ici le statut via l'API, mais pour l'UX simple :
    return render(request, 'donations/success.html')

def payment_cancel(request):
    return render(request, 'donations/cancel.html')

# --- Webhook (Notification Serveur à Serveur) ---
# C'est ici que MaxiCash confirmera le paiement en arrière-plan
@csrf_exempt 
def payment_ipn(request):
    if request.method == 'POST':
        reference = request.POST.get('reference')
        status = request.POST.get('status') # Vérifier le paramètre exact dans la doc MaxiCash
        
        try:
            donation = Donation.objects.get(reference=reference)
            if status == 'SUCCESS': # Ou le code succès de MaxiCash (ex: "00")
                donation.status = 'SUCCESS'
                donation.save()
                # Ici: Envoyer un email de remerciement automatique
        except Donation.DoesNotExist:
            pass
            
    return HttpResponse("OK")