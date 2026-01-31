from django.db import models

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('COORD', 'Coordination Générale'),
        ('TERRAIN', 'Opérations & Terrain'),
        ('COM', 'Communication & Partenariats'),
        ('TECH', 'Support Technique & Logistique'),
        ('BENEVOLE', 'Bénévole'),
    )

    name = models.CharField(max_length=100, verbose_name="Nom complet")
    role = models.CharField(max_length=100, verbose_name="Titre du poste", default="Bénévole", help_text="Ex: Coordonnateur Principal")
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    category = models.CharField(max_length=20, choices=ROLE_CHOICES, default='BENEVOLE', verbose_name="Département")
    bio = models.TextField(blank=True, verbose_name="Courte biographie")
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    facebook_url = models.URLField(blank=True, verbose_name="Lien Facebook")
    linkedin_url = models.URLField(blank=True, verbose_name="Lien LinkedIn")
    twitter_url = models.URLField(blank=True, verbose_name="Lien Twitter/X")
    
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage", help_text="Plus petit = affiché en premier")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Équipe PNAC"
        ordering = ['order', 'name']

class VolunteerApplication(models.Model):
    NOTIFICATION_CHOICES = (
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Rejeté'),
    )

    full_name = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    message = models.TextField(verbose_name="Message de motivation", blank=True)
    preferred_notification = models.CharField(
        max_length=10, 
        choices=NOTIFICATION_CHOICES, 
        default='EMAIL',
        verbose_name="Mode de communication préféré"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de soumission")

    def __str__(self):
        return f"Candidature de {self.full_name} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Demande d'adhésion"
        verbose_name_plural = "Demandes d'adhésion"
        ordering = ['-created_at']
