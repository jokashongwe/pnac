from modeltranslation.translator import register, TranslationOptions
from .models import CarouselItem

@register(CarouselItem)
class CarouselTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'button_text')