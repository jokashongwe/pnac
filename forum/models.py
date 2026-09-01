from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Topic(models.Model):
    ACCESS_OPEN = "OPEN"
    ACCESS_RESTRICTED = "RESTRICTED"
    ACCESS_CHOICES = (
        (ACCESS_OPEN, _("Ouvert")),
        (ACCESS_RESTRICTED, _("Accès restreint")),
    )

    title = models.CharField(max_length=200, verbose_name=_("Sujet de discussion"))
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name=_("Message d'introduction"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Modérateur (compte)"),
    )
    created_by = models.ForeignKey(
        "team.TeamMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_topics",
        verbose_name=_("Créé par"),
    )
    access_mode = models.CharField(
        max_length=20,
        choices=ACCESS_CHOICES,
        default=ACCESS_OPEN,
        verbose_name=_("Mode d'accès"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Discussion ouverte ?"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Sujet / Discussion")
        verbose_name_plural = _("Sujets / Discussions")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "sujet"
            slug = base
            index = 2
            while Topic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{index}"
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_post_count(self):
        return self.posts.count()

    def is_restricted(self):
        return self.access_mode == self.ACCESS_RESTRICTED


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(
        "team.TeamMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="forum_posts",
        verbose_name=_("Auteur"),
    )
    visitor_name = models.CharField(
        max_length=50,
        verbose_name=_("Nom du visiteur"),
        default="Citoyen",
        blank=True,
    )
    content = models.TextField(verbose_name=_("Message"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Réaction / Message")
        verbose_name_plural = _("Réactions / Messages")

    def __str__(self):
        return f"Message de {self.display_name()} sur {self.topic}"

    def display_name(self):
        if self.author_id:
            return self.author.name
        return self.visitor_name or _("Citoyen")


class TopicAccessRequest(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_DENIED = "DENIED"
    STATUS_CHOICES = (
        (STATUS_PENDING, _("En attente")),
        (STATUS_APPROVED, _("Approuvé")),
        (STATUS_DENIED, _("Refusé")),
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="access_requests",
        verbose_name=_("Sujet"),
    )
    member = models.ForeignKey(
        "team.TeamMember",
        on_delete=models.CASCADE,
        related_name="topic_access_requests",
        verbose_name=_("Membre"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name=_("Statut"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        "team.TeamMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_access_requests",
        verbose_name=_("Traité par"),
    )

    class Meta:
        verbose_name = _("Demande d'accès")
        verbose_name_plural = _("Demandes d'accès")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["topic", "member"], name="unique_topic_member_access"),
        ]

    def __str__(self):
        return f"{self.member} → {self.topic} ({self.status})"
