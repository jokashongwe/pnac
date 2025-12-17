from django.shortcuts import render
from .models import Resource

def resource_list(request):
    # On récupère tout ce qui est public
    all_resources = Resource.objects.filter(is_public=True).order_by('-created_at')
    
    # On peut pré-filtrer pour l'affichage si besoin, ou laisser le template gérer
    context = {
        'guides': all_resources.filter(category='GUIDE'),
        'reports': all_resources.filter(category='REPORT'),
        'tools': all_resources.filter(category__in=['TOOL', 'LEGAL']),
    }
    return render(request, 'resources/list.html', context)