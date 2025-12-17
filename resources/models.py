from django.db import models
import os

class Resource(models.Model):
    CATEGORY_CHOICES = (
        ('GUIDE', 'Guides & Sensibilisation'),   # Pour l'éducation citoyenne 
        ('REPORT', 'Rapports & Transparence'),   # Pour la transparence 
        ('TOOL', 'Outils Salongo & Technique'),  # Pour les actions communautaires
        ('LEGAL', 'Documents Officiels'),
    )

    title = models.CharField(max_length=200, verbose_name="Titre du document")
    description = models.TextField(blank=True, verbose_name="Courte description")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GUIDE')
    
    file = models.FileField(upload_to='resources/docs/', verbose_name="Fichier (PDF)")
    cover_image = models.ImageField(upload_to='resources/covers/', blank=True, null=True, verbose_name="Image de couverture (Optionnel)")
    
    is_public = models.BooleanField(default=True, verbose_name="Visible sur le site")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Petite fonction pour afficher la taille du fichier (UX)
    def file_size(self):
        try:
            size = self.file.size
            if size > 1000000:
                return f"{size / 1000000:.1f} MB"
            return f"{size / 1000:.0f} KB"
        except:
            return "N/A"
            
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.upper().replace('.', '')