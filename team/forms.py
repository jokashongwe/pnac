from django import forms
from .models import VolunteerApplication

class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['full_name', 'email', 'phone', 'message', 'preferred_notification']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pnacGreen focus:border-transparent outline-none transition',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pnacGreen focus:border-transparent outline-none transition',
                'placeholder': 'votre.email@exemple.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pnacGreen focus:border-transparent outline-none transition',
                'placeholder': '+243 ...'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pnacGreen focus:border-transparent outline-none transition',
                'placeholder': 'Dites-nous pourquoi vous voulez rejoindre notre équipe...',
                'rows': 4
            }),
            'preferred_notification': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pnacGreen focus:border-transparent outline-none transition'
            }),
        }
