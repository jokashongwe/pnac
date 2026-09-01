from team.decorators import get_member


def member_context(request):
    member = get_member(getattr(request, "user", None))
    return {
        "current_member": member,
        "is_forum_moderator": bool(member and member.is_moderator()),
    }
