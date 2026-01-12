from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['visitor_name', 'content']
        widgets = {
            'visitor_name': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-pnacBlue focus:border-pnacBlue',
                'placeholder': 'Votre nom ou pseudo'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-pnacBlue focus:border-pnacBlue',
                'rows': 3,
                'placeholder': 'Partagez votre avis ou signalez un problème...'
            }),
        }