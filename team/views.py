from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TeamMember, VolunteerApplication
from .forms import VolunteerApplicationForm

def team_page(request):
    # On récupère tous les membres
    members = TeamMember.objects.all()
    
    # On peut passer les catégories distinctes si on veut faire des onglets, 
    # ou simplement passer la liste complète et trier dans le template.
    
    # Exemple de regroupement simple pour le template
    leadership = members.filter(category='COORD')
    operations = members.filter(category='TERRAIN')
    others = members.exclude(category__in=['COORD', 'TERRAIN'])

    context = {
        'leadership': leadership,
        'operations': operations,
        'others': others,
        'all_members': members # Fallback
    }
    return render(request, 'team.html', context)

def volunteer_apply(request):
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            
            # Notification Logic
            if application.preferred_notification == 'EMAIL':
                # Code pour envoyer un email
                print(f"Simulation d'envoi d'email à {application.email}: Bienvenue dans l'équipe PNAC !")
            else:
                # Code pour envoyer un SMS
                print(f"Simulation d'envoi de SMS à {application.phone}: PNAC - Merci pour votre candidature !")
            
            messages.success(request, "Votre demande d'adhésion a été envoyée avec succès ! Nous vous contacterons bientôt.")
            return redirect('home')
    else:
        form = VolunteerApplicationForm()
    
    return render(request, 'team/volunteer_apply.html', {'form': form})
