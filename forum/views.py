from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Topic
from .forms import PostForm

def forum_index(request):
    """Affiche la liste des sujets créés par l'admin"""
    topics = Topic.objects.filter(is_active=True)
    return render(request, 'forum/index.html', {'topics': topics})

def topic_detail(request, slug):
    """Affiche un sujet et ses messages, plus le formulaire de réponse"""
    topic = get_object_or_404(Topic, slug=slug, is_active=True)
    posts = topic.posts.all()
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.save()
            messages.success(request, "Votre message a été publié avec succès !")
            return redirect('topic_detail', slug=slug)
    else:
        form = PostForm()

    context = {
        'topic': topic,
        'posts': posts,
        'form': form,
        'post_count': posts.count()
    }
    return render(request, 'forum/detail.html', context)