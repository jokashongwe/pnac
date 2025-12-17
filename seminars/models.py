from django.db import models
import uuid

class Seminar(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de la conférence")
    description = models.TextField()
    image = models.ImageField(upload_to='seminars/', blank=True, null=True)
    
    start_date = models.DateTimeField(verbose_name="Début")
    end_date = models.DateTimeField(verbose_name="Fin")
    location = models.CharField(max_length=200, verbose_name="Lieu (Hôtel/Salle)")
    
    # Tarification
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Frais d'inscription ($)")
    accommodation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Frais Hébergement / Nuit ($)", help_text="Laisser à 0 si non proposé")
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class SeminarRegistration(models.Model):
    TYPE_CHOICES = (
        ('PARTICIPANT', 'Participant Individuel'),
        ('PARTNER', 'Partenaire / Sponsor'),
        ('SPEAKER', 'Intervenant'),
    )
    
    ORIGIN_CHOICES = (
        ('LOCAL', 'National (RDC)'),
        ('INTL', 'International (Étranger)'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'En attente de paiement'),
        ('CONFIRMED', 'Confirmé & Payé'),
        ('CANCELLED', 'Annulé'),
    )

    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE, related_name='registrations')
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.CharField(max_length=100, blank=True, verbose_name="Organisation / Entreprise")
    phone = models.CharField(max_length=20)
    
    participant_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='PARTICIPANT')
    origin = models.CharField(max_length=10, choices=ORIGIN_CHOICES, default='LOCAL')
    
    # Logistique
    needs_accommodation = models.BooleanField(default=False, verbose_name="Besoin d'hébergement")
    accommodation_nights = models.PositiveIntegerField(default=0, verbose_name="Nombre de nuits")
    
    # Financier
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcul automatique du total avant sauvegarde
        total = self.seminar.registration_fee
        if self.needs_accommodation:
            total += (self.seminar.accommodation_fee * self.accommodation_nights)
        self.total_amount = total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.seminar.title}"