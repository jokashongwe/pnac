from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Donation

def donate(request):
    if request.method == 'POST':
        try:
            amount = request.POST.get('amount')
            email = request.POST.get('email')
            name = request.POST.get('name') or "Anonyme"
            is_anonymous = request.POST.get('anonymous') == 'on'

            Donation.objects.create(
                amount=amount,
                email=email,
                donor_name="Anonyme" if is_anonymous else name,
                is_anonymous=is_anonymous
            )

            messages.success(request, "Merci pour votre générosité ! Votre soutien aide à assainir nos quartiers.")
            return redirect('home')
            
        except Exception as e:
            messages.error(request, "Une erreur est survenue. Vérifiez le montant.")
            
    return render(request, 'donations/index.html')