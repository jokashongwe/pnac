from modeltranslation.translator import register, TranslationOptions
from .models import Event

@register(Event)
class CarouselTranslationOptions(TranslationOptions):
    fields = ('title', 'description')