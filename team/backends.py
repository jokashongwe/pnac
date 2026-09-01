from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import TeamMember
from .phone import normalize_phone


class MemberAuthBackend(ModelBackend):
    """Authenticate a TeamMember with email or phone + password."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = (username or "").strip()
        if not identifier or not password:
            return None

        phone = normalize_phone(identifier)
        lookup = Q(email__iexact=identifier.lower())
        if phone:
            lookup |= Q(phone=phone)

        member = (
            TeamMember.objects.select_related("user")
            .filter(lookup, user__isnull=False, user__is_active=True)
            .first()
        )
        if member is None:
            return None
        user = member.user
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
