from django.db import models

class Event(models.Model):
    TYPES = (
        ('SALONGO', 'Salongo Populaire'),
        ('FORMATION', 'Formation & Sensibilisation'),
        ('CAMPAGNE', 'Campagne de Salubrité'),
    )
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=TYPES, default='SALONGO')
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255, help_text="Commune ou Quartier (ex: Kinshasa)")
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d/%m/%Y')}"

class Volunteer(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('PRESENT', 'Présent sur le terrain'),
    )

    ROLE_CHOICES = (
        ('PARTICIPANT', 'Participant Salongo'),
        ('LEADER', 'Chef de Quartier / Leader'), # [cite: 22]
        ('ECO_BRIGADE', 'Membre Eco-Brigade'),   # [cite: 14]
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='volunteers', verbose_name="Événement ciblé")
    full_name = models.CharField(max_length=100, verbose_name="Nom Complet")
    phone = models.CharField(max_length=20, verbose_name="Téléphone", help_text="Essentiel pour la coordination terrain")
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PARTICIPANT')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"

    class Meta:
        verbose_name = "Bénévole / Participant"
        verbose_name_plural = "Gestion des Bénévoles"