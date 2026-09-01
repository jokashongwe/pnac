from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from forum.forms import PostForm
from forum.models import Post, Topic, TopicAccessRequest
from forum.permissions import can_post_on_topic, can_read_topic, get_access_request
from team.decorators import get_member, member_required, moderator_required


def _visible_topics(member):
    qs = Topic.objects.filter(is_active=True)
    if member and member.is_moderator():
        return qs
    open_qs = qs.filter(access_mode=Topic.ACCESS_OPEN)
    if not member:
        return open_qs
    approved_ids = TopicAccessRequest.objects.filter(
        member=member,
        status=TopicAccessRequest.STATUS_APPROVED,
    ).values_list("topic_id", flat=True)
    return qs.filter(pk__in=list(approved_ids)) | open_qs


def forum_index(request):
    member = get_member(request.user)
    topics = _visible_topics(member).select_related("created_by", "author").distinct()
    return render(request, "forum/index.html", {"topics": topics, "member": member})


def topic_detail(request, slug):
    topic = get_object_or_404(Topic, slug=slug, is_active=True)
    member = get_member(request.user)
    access_request = get_access_request(member, topic)

    if not can_read_topic(member, topic):
        if topic.access_mode == Topic.ACCESS_RESTRICTED:
            if member is None:
                messages.info(request, _("Connectez-vous pour demander l'accès à ce sujet."))
                return redirect("member_login")
            return render(
                request,
                "forum/restricted.html",
                {"topic": topic, "member": member, "access_request": access_request},
            )
        return redirect("forum_index")

    posts = topic.posts.select_related("author").all()
    form = None
    can_post = can_post_on_topic(member, topic)
    if can_post:
        form = PostForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = member
            post.visitor_name = member.name
            post.save()
            messages.success(request, _("Votre message a été publié avec succès !"))
            return redirect("topic_detail", slug=slug)
    elif request.method == "POST":
        messages.error(request, _("Vous n'êtes pas autorisé à publier sur ce sujet."))
        return redirect("topic_detail", slug=slug)

    return render(
        request,
        "forum/detail.html",
        {
            "topic": topic,
            "posts": posts,
            "form": form,
            "post_count": posts.count(),
            "member": member,
            "can_post": can_post,
            "is_moderator": bool(member and member.is_moderator()),
            "access_request": access_request,
        },
    )


@member_required
@require_POST
def request_topic_access(request, slug):
    topic = get_object_or_404(Topic, slug=slug, is_active=True, access_mode=Topic.ACCESS_RESTRICTED)
    member = request.member
    if member.is_forum_banned:
        messages.error(request, _("Votre accès au forum a été suspendu."))
        return redirect("member_dashboard")
    if member.is_moderator() or can_read_topic(member, topic):
        return redirect("topic_detail", slug=slug)

    existing = get_access_request(member, topic)
    if existing and existing.status == TopicAccessRequest.STATUS_PENDING:
        messages.info(request, _("Votre demande est déjà en cours d'examen."))
    elif existing and existing.status == TopicAccessRequest.STATUS_APPROVED:
        return redirect("topic_detail", slug=slug)
    elif existing and existing.status == TopicAccessRequest.STATUS_DENIED:
        existing.status = TopicAccessRequest.STATUS_PENDING
        existing.reviewed_at = None
        existing.reviewed_by = None
        existing.save(update_fields=["status", "reviewed_at", "reviewed_by"])
        messages.success(request, _("Votre demande d'accès a été renvoyée."))
    else:
        TopicAccessRequest.objects.create(topic=topic, member=member)
        messages.success(request, _("Votre demande d'accès a été envoyée."))
    return redirect("topic_detail", slug=slug)


@moderator_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    slug = post.topic.slug
    post.delete()
    messages.success(request, _("Le message a été supprimé."))
    return redirect("topic_detail", slug=slug)
