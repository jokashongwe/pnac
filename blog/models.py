from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class Post(models.Model):
    CATEGORY_CHOICES = (
        ("NEWS", _("Actualités")),
        ("STORY", _("Histoires de succès")),
        ("PRESS", _("Communiqués de presse")),
    )

    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    slug = models.SlugField(unique=True, blank=True, help_text=_("Laisser vide pour générer automatiquement"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Auteur"))

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="NEWS")
    image = models.ImageField(upload_to="blog/", verbose_name=_("Image à la une"))

    excerpt = models.TextField(max_length=300, verbose_name=_("Extrait (Introduction)"))
    content = RichTextField(verbose_name=_("Contenu de l'article"))

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Article")
        verbose_name_plural = _("Blog & Actualités")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
