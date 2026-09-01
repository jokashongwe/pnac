from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from forum.models import Topic
from .models import VolunteerApplication

INPUT_CLASS = (
    "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 "
    "focus:ring-pnacGreen focus:border-transparent outline-none transition"
)


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ["full_name", "email", "phone", "message", "preferred_notification"]
        labels = {
            "full_name": _("Nom complet"),
            "email": _("Email"),
            "phone": _("Téléphone"),
            "message": _("Message de motivation"),
            "preferred_notification": _("Mode de communication préféré"),
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": _("Votre nom complet")}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": _("votre.email@exemple.com")}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "+243 ..."}),
            "message": forms.Textarea(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": _("Dites-nous pourquoi vous voulez rejoindre notre équipe..."),
                    "rows": 4,
                }
            ),
            "preferred_notification": forms.Select(attrs={"class": INPUT_CLASS}),
        }


class MemberLoginForm(forms.Form):
    identifier = forms.CharField(
        label=_("Email ou téléphone"),
        widget=forms.TextInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": _("email@exemple.com ou +243 ..."),
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASS, "autocomplete": "current-password"}
        ),
    )


class OtpForm(forms.Form):
    code = forms.CharField(
        label=_("Code de vérification"),
        min_length=6,
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "class": INPUT_CLASS + " text-center tracking-[0.4em] text-xl font-bold",
                "inputmode": "numeric",
                "autocomplete": "one-time-code",
                "placeholder": "000000",
            }
        ),
    )


class MemberPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description", "access_mode", "is_active"]
        labels = {
            "title": _("Titre"),
            "description": _("Introduction"),
            "access_mode": _("Mode d'accès"),
            "is_active": _("Discussion ouverte"),
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 6}),
            "access_mode": forms.Select(attrs={"class": INPUT_CLASS}),
            "is_active": forms.CheckboxInput(
                attrs={"class": "h-4 w-4 text-pnacGreen border-gray-300 rounded"}
            ),
        }
