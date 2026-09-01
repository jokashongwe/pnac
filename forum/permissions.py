from forum.models import Topic, TopicAccessRequest


def is_moderator(member):
    return bool(member and member.is_moderator())


def can_read_topic(member, topic):
    if topic.access_mode == Topic.ACCESS_OPEN:
        return True
    if is_moderator(member):
        return True
    if not member:
        return False
    return TopicAccessRequest.objects.filter(
        member=member,
        topic=topic,
        status=TopicAccessRequest.STATUS_APPROVED,
    ).exists()


def can_post_on_topic(member, topic):
    if not member or member.is_forum_banned:
        return False
    if not topic.is_active:
        return False
    if is_moderator(member):
        return True
    if topic.access_mode == Topic.ACCESS_OPEN:
        return True
    return TopicAccessRequest.objects.filter(
        member=member,
        topic=topic,
        status=TopicAccessRequest.STATUS_APPROVED,
    ).exists()


def get_access_request(member, topic):
    if not member:
        return None
    return TopicAccessRequest.objects.filter(member=member, topic=topic).first()
