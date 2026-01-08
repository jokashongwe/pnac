from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    
    # Filtre par catégorie si demandé dans l'URL (?cat=NEWS)
    category = request.GET.get('cat')
    if category:
        posts = posts.filter(category=category)
        
    return render(request, 'blog/list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    # Suggestions (3 autres articles récents)
    related_posts = Post.objects.filter(is_published=True).exclude(id=post.id)[:3]
    
    return render(request, 'blog/detail.html', {'post': post, 'related_posts': related_posts})