from django.db import models

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('COORD', 'Coordination Générale'),
        ('TERRAIN', 'Opérations & Terrain'),
        ('COM', 'Communication & Partenariats'),
        ('TECH', 'Support Technique & Logistique'),
    )

    name = models.CharField(max_length=100, verbose_name="Nom complet")
    role = models.CharField(max_length=100, verbose_name="Titre du poste", help_text="Ex: Coordonnateur Principal")
    category = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TERRAIN', verbose_name="Département")
    bio = models.TextField(blank=True, verbose_name="Courte biographie")
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, verbose_name="Lien LinkedIn")
    twitter_url = models.URLField(blank=True, verbose_name="Lien Twitter/X")
    
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage", help_text="Plus petit = affiché en premier")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Équipe PNAC"
        ordering = ['order', 'name']