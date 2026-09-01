from django.urls import path

from team.space_views import (
    member_dashboard,
    member_login,
    member_logout,
    member_otp,
    member_otp_resend,
    member_password,
    moderation_member_ban,
    moderation_members,
    moderation_request_review,
    moderation_requests,
    moderation_topic_create,
)

urlpatterns = [
    path("connexion/", member_login, name="member_login"),
    path("deconnexion/", member_logout, name="member_logout"),
    path("otp/", member_otp, name="member_otp"),
    path("otp/renvoyer/", member_otp_resend, name="member_otp_resend"),
    path("", member_dashboard, name="member_dashboard"),
    path("mot-de-passe/", member_password, name="member_password"),
    path("moderation/sujets/nouveau/", moderation_topic_create, name="moderation_topic_create"),
    path("moderation/demandes/", moderation_requests, name="moderation_requests"),
    path(
        "moderation/demandes/<int:request_id>/<str:action>/",
        moderation_request_review,
        name="moderation_request_review",
    ),
    path("moderation/membres/", moderation_members, name="moderation_members"),
    path("moderation/membres/<int:member_id>/bannir/", moderation_member_ban, name="moderation_member_ban"),
]
