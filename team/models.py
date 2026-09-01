from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .phone import normalize_phone


class TeamMember(models.Model):
    ROLE_CHOICES = (
        ("COORD", _("Coordination Générale")),
        ("TERRAIN", _("Opérations & Terrain")),
        ("COM", _("Communication & Partenariats")),
        ("TECH", _("Support Technique & Logistique")),
        ("BENEVOLE", _("Bénévole")),
    )

    MODERATOR_CATEGORIES = ("COORD", "COM")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="member_profile",
        verbose_name=_("Compte de connexion"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Nom complet"))
    role = models.CharField(
        max_length=100,
        verbose_name=_("Titre du poste"),
        default="Bénévole",
        help_text=_("Ex: Coordonnateur Principal"),
    )
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Téléphone"))
    category = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="BENEVOLE",
        verbose_name=_("Département"),
    )
    bio = models.TextField(blank=True, verbose_name=_("Courte biographie"))
    photo = models.ImageField(upload_to="team_photos/", blank=True, null=True)
    facebook_url = models.URLField(blank=True, verbose_name=_("Lien Facebook"))
    linkedin_url = models.URLField(blank=True, verbose_name=_("Lien LinkedIn"))
    twitter_url = models.URLField(blank=True, verbose_name=_("Lien Twitter/X"))
    phone_verified = models.BooleanField(default=False, verbose_name=_("Téléphone vérifié"))
    is_forum_banned = models.BooleanField(default=False, verbose_name=_("Banni du forum"))
    order = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage"),
        help_text=_("Plus petit = affiché en premier"),
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        normalized = normalize_phone(self.phone)
        self.phone = normalized or None
        if self.email:
            self.email = self.email.strip().lower()
        else:
            self.email = None
        if not self.phone:
            self.phone_verified = False
        super().save(*args, **kwargs)

    def is_moderator(self):
        return self.category in self.MODERATOR_CATEGORIES

    def has_login(self):
        return self.user_id is not None

    def needs_phone_verification(self):
        return bool(self.phone) and not self.phone_verified

    def can_open_space(self):
        return bool(self.email or self.phone)

    class Meta:
        verbose_name = _("Membre de l'équipe")
        verbose_name_plural = _("Équipe PNAC")
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(email__isnull=False),
                name="unique_member_email",
            ),
            models.UniqueConstraint(
                fields=["phone"],
                condition=models.Q(phone__isnull=False),
                name="unique_member_phone",
            ),
        ]


class PhoneOTP(models.Model):
    member = models.ForeignKey(
        TeamMember,
        on_delete=models.CASCADE,
        related_name="otp_codes",
        verbose_name=_("Membre"),
    )
    code_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Code OTP")
        verbose_name_plural = _("Codes OTP")
        ordering = ["-created_at"]

    def __str__(self):
        return f"OTP {self.member} ({self.created_at:%Y-%m-%d %H:%M})"


class VolunteerApplication(models.Model):
    NOTIFICATION_CHOICES = (
        ("EMAIL", "Email"),
        ("SMS", "SMS"),
    )

    STATUS_CHOICES = (
        ("PENDING", _("En attente")),
        ("APPROVED", _("Approuvé")),
        ("REJECTED", _("Rejeté")),
    )

    full_name = models.CharField(max_length=100, verbose_name=_("Nom complet"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, verbose_name=_("Téléphone"))
    message = models.TextField(verbose_name=_("Message de motivation"), blank=True)
    preferred_notification = models.CharField(
        max_length=10,
        choices=NOTIFICATION_CHOICES,
        default="EMAIL",
        verbose_name=_("Mode de communication préféré"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
        verbose_name=_("Statut"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de soumission"))

    def __str__(self):
        return f"Candidature de {self.full_name} ({self.get_status_display()})"

    class Meta:
        verbose_name = _("Demande d'adhésion")
        verbose_name_plural = _("Demandes d'adhésion")
        ordering = ["-created_at"]
