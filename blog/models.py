from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Post(models.Model):
    CATEGORY_CHOICES = (
        ('NEWS', 'Actualités'),
        ('STORY', 'Histoires de succès'),
        ('PRESS', 'Communiqués de presse'),
    )

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, help_text="Laisser vide pour générer automatiquement")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='NEWS')
    image = models.ImageField(upload_to='blog/', verbose_name="Image à la une")
    
    # Contenu principal
    excerpt = models.TextField(max_length=300, verbose_name="Extrait (Introduction)")
    content = models.TextField(verbose_name="Contenu de l'article")
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Blog & Actualités"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)