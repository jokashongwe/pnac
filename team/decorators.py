from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from team.models import TeamMember

OTP_EXEMPT_URL_NAMES = {"member_otp", "member_otp_resend", "member_logout", "member_login"}


def get_member(user):
    if not user or not user.is_authenticated:
        return None
    return TeamMember.objects.filter(user=user).first()


def member_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        member = get_member(request.user)
        if member is None:
            messages.error(request, _("Connectez-vous avec votre espace membre."))
            return redirect("member_login")
        url_name = getattr(request.resolver_match, "url_name", "")
        if member.needs_phone_verification() and url_name not in OTP_EXEMPT_URL_NAMES:
            return redirect("member_otp")
        request.member = member
        return view_func(request, *args, **kwargs)

    return wrapper


def moderator_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        inner = member_required(_moderator_gate(view_func))
        return inner(request, *args, **kwargs)

    return wrapper


def _moderator_gate(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.member.is_moderator():
            messages.error(
                request,
                _("Cette action est réservée à la coordination et à la communication."),
            )
            return redirect("member_dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper
