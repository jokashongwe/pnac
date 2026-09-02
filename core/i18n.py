from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import translate_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language, get_language_from_path, override
from django.views.i18n import LANGUAGE_QUERY_PARAMETER


def _language_codes():
    return [code for code, _name in settings.LANGUAGES]


def _swap_language_prefix(url, lang_code):
    parsed = urlsplit(url)
    path = parsed.path or "/"
    parts = path.split("/")
    codes = _language_codes()
    if len(parts) > 1 and parts[1] in codes:
        parts[1] = lang_code
        new_path = "/".join(parts)
    elif path.startswith("/"):
        new_path = f"/{lang_code}{path}"
    else:
        return url
    return urlunsplit((parsed.scheme, parsed.netloc, new_path, parsed.query, parsed.fragment))


def set_language(request):
    """Like Django's set_language, but can rewrite /fr/… → /en/… even when the
    request language comes from the browser (Accept-Language: en)."""
    next_url = request.POST.get("next", request.GET.get("next"))
    if (
        next_url or request.accepts("text/html")
    ) and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get("HTTP_REFERER")
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = "/"

    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)
    if request.method != "POST":
        return response

    lang_code = request.POST.get(LANGUAGE_QUERY_PARAMETER)
    if not (lang_code and check_for_language(lang_code)):
        return response

    if next_url:
        path_lang = get_language_from_path(urlsplit(next_url).path)
        if path_lang:
            with override(path_lang):
                next_trans = translate_url(next_url, lang_code)
        else:
            next_trans = translate_url(next_url, lang_code)
        if next_trans == next_url:
            next_trans = _swap_language_prefix(next_url, lang_code)
        response = HttpResponseRedirect(next_trans)

    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    return response
