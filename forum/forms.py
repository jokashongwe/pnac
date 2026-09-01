from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        labels = {
            "content": _("Votre Message"),
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "w-full border-gray-300 rounded-md shadow-sm focus:ring-pnacBlue focus:border-pnacBlue p-3 border",
                    "rows": 4,
                    "placeholder": _("Partagez votre avis ou signalez un problème..."),
                }
            ),
        }
