from modeltranslation.translator import register, TranslationOptions
from .models import TeamMember

@register(TeamMember)
class CarouselTranslationOptions(TranslationOptions):
    fields = ('name', 'role', 'category', 'bio')