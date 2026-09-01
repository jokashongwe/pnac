from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


def provision_member_access(member, password):
    if not member.can_open_space():
        raise ValueError(_("Le membre doit avoir un email ou un téléphone pour ouvrir un accès."))

    if member.user_id:
        user = member.user
        user.set_password(password)
        if member.email:
            user.email = member.email
        user.first_name = member.name[:150]
        user.is_active = True
        user.save()
        return user

    base = (member.email or f"m{member.pk}_{member.phone or 'member'}")[:140]
    username = base
    suffix = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}_{suffix}"
        suffix += 1

    user = User.objects.create_user(
        username=username,
        email=member.email or "",
        password=password,
        first_name=member.name[:150],
    )
    member.user = user
    if not member.phone:
        member.phone_verified = False
    member.save(update_fields=["user", "phone_verified"])
    return user
