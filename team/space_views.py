from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from forum.models import Post, Topic, TopicAccessRequest
from forum.permissions import can_read_topic
from team.decorators import get_member, member_required, moderator_required
from team.forms import MemberLoginForm, MemberPasswordChangeForm, OtpForm, TopicCreateForm
from team.models import TeamMember
from team.services.otp import OtpError, issue_otp, verify_otp


def _safe_next(request):
    nxt = request.POST.get("next") or request.GET.get("next")
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        return nxt
    return None


def member_login(request):
    member = get_member(request.user)
    if member:
        if member.needs_phone_verification():
            return redirect("member_otp")
        return redirect("member_dashboard")

    form = MemberLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["identifier"],
            password=form.cleaned_data["password"],
        )
        if user is None or get_member(user) is None:
            messages.error(request, _("Identifiant ou mot de passe incorrect."))
        else:
            login(request, user)
            member = get_member(user)
            if member.needs_phone_verification():
                try:
                    issue_otp(member)
                    messages.info(request, _("Un code de vérification a été envoyé par SMS."))
                except OtpError as exc:
                    messages.error(request, str(exc))
                return redirect("member_otp")
            return redirect(_safe_next(request) or "member_dashboard")

    return render(request, "team/space/login.html", {"form": form, "next": request.GET.get("next", "")})


def member_logout(request):
    logout(request)
    messages.success(request, _("Vous êtes déconnecté."))
    return redirect("member_login")


@member_required
def member_otp(request):
    member = request.member
    if not member.needs_phone_verification():
        return redirect("member_dashboard")

    form = OtpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            verify_otp(member, form.cleaned_data["code"])
            messages.success(request, _("Votre numéro de téléphone a été vérifié."))
            return redirect(_safe_next(request) or "member_dashboard")
        except OtpError as exc:
            messages.error(request, str(exc))

    return render(
        request,
        "team/space/otp.html",
        {"form": form, "phone": member.phone},
    )


@member_required
@require_POST
def member_otp_resend(request):
    member = request.member
    if not member.needs_phone_verification():
        return redirect("member_dashboard")
    try:
        issue_otp(member)
        messages.success(request, _("Un nouveau code a été envoyé par SMS."))
    except OtpError as exc:
        messages.error(request, str(exc))
    return redirect("member_otp")


@member_required
def member_dashboard(request):
    member = request.member
    open_topics = Topic.objects.filter(is_active=True, access_mode=Topic.ACCESS_OPEN)
    restricted_topics = Topic.objects.filter(is_active=True, access_mode=Topic.ACCESS_RESTRICTED)
    requests_by_topic = {
        req.topic_id: req
        for req in TopicAccessRequest.objects.filter(member=member, topic__in=restricted_topics)
    }
    restricted_rows = []
    for topic in restricted_topics:
        if not can_read_topic(member, topic) and not member.is_moderator():
            # still list so they can request access
            pass
        restricted_rows.append({"topic": topic, "request": requests_by_topic.get(topic.id)})

    my_posts = Post.objects.filter(author=member).select_related("topic").order_by("-created_at")[:8]
    pending_count = 0
    if member.is_moderator():
        pending_count = TopicAccessRequest.objects.filter(status=TopicAccessRequest.STATUS_PENDING).count()

    return render(
        request,
        "team/space/dashboard.html",
        {
            "member": member,
            "open_topics": open_topics,
            "restricted_rows": restricted_rows,
            "my_posts": my_posts,
            "pending_count": pending_count,
        },
    )


@member_required
def member_password(request):
    form = MemberPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, _("Votre mot de passe a été mis à jour."))
        return redirect("member_dashboard")
    return render(request, "team/space/password.html", {"form": form})


@moderator_required
def moderation_topic_create(request):
    form = TopicCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        topic = form.save(commit=False)
        topic.created_by = request.member
        topic.author = request.user
        topic.save()
        messages.success(request, _("Le sujet a été créé."))
        return redirect("topic_detail", slug=topic.slug)
    return render(request, "team/moderation/topic_form.html", {"form": form})


@moderator_required
def moderation_requests(request):
    pending = (
        TopicAccessRequest.objects.filter(status=TopicAccessRequest.STATUS_PENDING)
        .select_related("member", "topic")
        .order_by("created_at")
    )
    recent = (
        TopicAccessRequest.objects.exclude(status=TopicAccessRequest.STATUS_PENDING)
        .select_related("member", "topic", "reviewed_by")[:20]
    )
    return render(
        request,
        "team/moderation/requests.html",
        {"pending": pending, "recent": recent},
    )


@moderator_required
@require_POST
def moderation_request_review(request, request_id, action):
    access = get_object_or_404(TopicAccessRequest, pk=request_id)
    if action not in ("approve", "deny"):
        return redirect("moderation_requests")
    access.status = (
        TopicAccessRequest.STATUS_APPROVED if action == "approve" else TopicAccessRequest.STATUS_DENIED
    )
    access.reviewed_by = request.member
    access.reviewed_at = timezone.now()
    access.save(update_fields=["status", "reviewed_by", "reviewed_at"])
    if action == "approve":
        messages.success(request, _("Accès accordé."))
    else:
        messages.success(request, _("Demande refusée."))
    return redirect("moderation_requests")


@moderator_required
def moderation_members(request):
    members = TeamMember.objects.filter(user__isnull=False).select_related("user").order_by("name")
    return render(request, "team/moderation/members.html", {"members": members})


@moderator_required
@require_POST
def moderation_member_ban(request, member_id):
    target = get_object_or_404(TeamMember, pk=member_id)
    if target.pk == request.member.pk:
        messages.error(request, _("Vous ne pouvez pas vous bannir vous-même."))
        return redirect("moderation_members")
    target.is_forum_banned = not target.is_forum_banned
    target.save(update_fields=["is_forum_banned"])
    if target.is_forum_banned:
        messages.success(request, _("Le membre a été banni du forum."))
    else:
        messages.success(request, _("Le bannissement a été levé."))
    return redirect("moderation_members")
