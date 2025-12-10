from django.shortcuts import render
from .models import TeamMember

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