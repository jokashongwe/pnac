import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class SmsError(Exception):
    pass


def _infobip_configured():
    return bool(getattr(settings, "INFOBIP_API_KEY", "") and getattr(settings, "INFOBIP_BASE_URL", ""))


def send_sms(to_number, text):
    """Send an SMS via Infobip. Returns True on success."""
    if not to_number:
        raise SmsError("Missing destination number")

    if not _infobip_configured():
        logger.warning("Infobip is not configured. SMS to %s: %s", to_number, text)
        return False

    base = settings.INFOBIP_BASE_URL.strip()
    if not base.startswith("http"):
        base = f"https://{base}"
    url = f"{base.rstrip('/')}/sms/2/text/advanced"
    payload = {
        "messages": [
            {
                "from": getattr(settings, "INFOBIP_SENDER", "PNAC") or "PNAC",
                "destinations": [{"to": to_number}],
                "text": text,
            }
        ]
    }
    headers = {
        "Authorization": f"App {settings.INFOBIP_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Infobip SMS failed for %s", to_number)
        raise SmsError(str(exc)) from exc
    return True
