from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.objects.filter(is_published=True).select_related("author")
    category = request.GET.get("cat")
    valid_categories = {code for code, _label in Post.CATEGORY_CHOICES}
    if category not in valid_categories:
        category = ""
    if category:
        posts = posts.filter(category=category)

    featured = posts.first() if posts.exists() else None
    others = posts[1:] if featured else posts

    return render(
        request,
        "blog/list.html",
        {
            "posts": posts,
            "featured": featured,
            "other_posts": others,
            "categories": Post.CATEGORY_CHOICES,
            "current_category": category,
            "current_category_label": dict(Post.CATEGORY_CHOICES).get(category, ""),
            "post_count": posts.count(),
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    related = list(
        Post.objects.filter(is_published=True, category=post.category)
        .exclude(id=post.id)
        .select_related("author")[:3]
    )
    if len(related) < 3:
        exclude_ids = [post.id, *[p.id for p in related]]
        related += list(
            Post.objects.filter(is_published=True)
            .exclude(id__in=exclude_ids)
            .select_related("author")[: 3 - len(related)]
        )

    return render(request, "blog/detail.html", {"post": post, "related_posts": related})
