from modeltranslation.translator import register, TranslationOptions
from .models import Seminar

@register(Seminar)
class CarouselTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'start_date', 'end_date')