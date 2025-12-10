from django.db import models
import uuid

class Donation(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('SUCCESS', 'Réussi'),
        ('FAILED', 'Échoué'),
    )
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # ID unique pour MaxiCash
    donor_name = models.CharField(max_length=100, verbose_name="Nom du donateur")
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant ($)")
    message = models.TextField(blank=True, null=True)
    date_donated = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reference} - {self.amount}$ ({self.status})"