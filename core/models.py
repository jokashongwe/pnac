from django.db import models

# Create your models here.
class CarouselItem(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre principal")
    subtitle = models.TextField(verbose_name="Sous-titre / Description")
    image = models.ImageField(upload_to='carousel/', verbose_name="Image de fond")
    
    # Boutons d'action (Optionnels)
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Texte du bouton")
    button_link = models.CharField(max_length=200, blank=True, verbose_name="Lien (ex: /donate)")
    
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        ordering = ['order']
        verbose_name = "Slide d'accueil"
        verbose_name_plural = "Carousel Accueil"

    def __str__(self):
        return self.title