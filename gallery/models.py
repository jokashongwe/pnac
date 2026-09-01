from django.db import models
from django.utils.translation import gettext_lazy as _

class GalleryImage(models.Model):
    CATEGORY_CHOICES = (
        ('SALONGO', _('Activités & Salongo')),
        ('SEMINAR', _('Séminaires & Conférences')),
        ('IMPACT', _('Impact (Avant/Après)')),
        ('TEAM', _('Vie d\'équipe')),
    )

    title = models.CharField(max_length=100, verbose_name="Titre / Lieu")
    image = models.ImageField(upload_to='gallery/showcase/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='SALONGO')
    description = models.TextField(blank=True, null=True, verbose_name="Légende (Optionnel)")
    date_taken = models.DateField(blank=True, null=True, verbose_name="Date de l'événement")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_taken', '-created_at']
        verbose_name = "Image Galerie"
        verbose_name_plural = "Galerie Multimédia"

    def __str__(self):
        return self.title