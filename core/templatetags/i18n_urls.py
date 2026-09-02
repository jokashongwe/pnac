from django import template
from django.conf import settings
from django.urls import translate_url
from django.utils.translation import override

register = template.Library()


def _language_codes():
    return [code for code, _name in settings.LANGUAGES]


@register.simple_tag(takes_context=True)
def translate_current_url(context, lang_code):
    """Same page in another language, even if the active language differs from the URL prefix."""
    request = context["request"]
    full_path = request.get_full_path()
    path = request.path
    codes = _language_codes()
    parts = path.split("/")
    current_prefix = parts[1] if len(parts) > 1 and parts[1] in codes else None

    if current_prefix:
        with override(current_prefix):
            translated = translate_url(full_path, lang_code)
        if translated != full_path:
            return translated
        parts[1] = lang_code
        new_path = "/".join(parts)
        query = request.META.get("QUERY_STRING")
        return f"{new_path}?{query}" if query else new_path

    with override(lang_code):
        translated = translate_url(full_path, lang_code)
    if translated != full_path:
        return translated
    return f"/{lang_code}{full_path}"
