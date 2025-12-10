from django.db import models

class Donation(models.Model):
    donor_name = models.CharField(max_length=100, verbose_name="Nom du donateur")
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant ($)")
    message = models.TextField(blank=True, null=True)
    date_donated = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donor_name} - {self.amount}$"