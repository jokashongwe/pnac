from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sujet de discussion")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="Message d'introduction")
    
    # L'admin qui crée le sujet
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Modérateur")
    
    is_active = models.BooleanField(default=True, verbose_name="Discussion ouverte ?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sujet / Discussion"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_post_count(self):
        return self.posts.count()


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    
    # Pour les visiteurs non connectés
    visitor_name = models.CharField(max_length=50, verbose_name="Nom du visiteur", default="Citoyen")
    content = models.TextField(verbose_name="Message")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Les messages s'affichent du plus ancien au plus récent (comme WhatsApp)
        verbose_name = "Réaction / Message"

    def __str__(self):
        return f"Message de {self.visitor_name} sur {self.topic}"