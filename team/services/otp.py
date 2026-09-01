import logging
import secrets
from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.utils.translation import get_language, gettext as _

from team.models import PhoneOTP
from team.services.sms import SmsError, send_sms

logger = logging.getLogger(__name__)

OTP_TTL_MINUTES = 10
OTP_RESEND_SECONDS = 60
OTP_MAX_ATTEMPTS = 5


class OtpError(Exception):
    pass


def _otp_message(code):
    if (get_language() or "fr").startswith("en"):
        return f"PNAC: your verification code is {code}. It expires in {OTP_TTL_MINUTES} minutes."
    return f"PNAC : votre code de vérification est {code}. Il expire dans {OTP_TTL_MINUTES} minutes."


def issue_otp(member):
    if not member.phone:
        raise OtpError(_("Aucun numéro de téléphone à vérifier."))

    latest = member.otp_codes.filter(used_at__isnull=True).order_by("-created_at").first()
    if latest and (timezone.now() - latest.created_at).total_seconds() < OTP_RESEND_SECONDS:
        raise OtpError(_("Veuillez patienter avant de demander un nouveau code."))

    code = f"{secrets.randbelow(1_000_000):06d}"
    now = timezone.now()
    PhoneOTP.objects.create(
        member=member,
        code_hash=make_password(code),
        expires_at=now + timedelta(minutes=OTP_TTL_MINUTES),
    )
    try:
        sent = send_sms(member.phone, _otp_message(code))
    except SmsError:
        logger.warning("OTP for member %s (%s): %s", member.pk, member.phone, code)
        raise OtpError(_("L'envoi du SMS a échoué. Réessayez dans un instant."))
    if not sent:
        logger.warning("OTP console fallback for member %s (%s): %s", member.pk, member.phone, code)
    return True


def verify_otp(member, raw_code):
    otp = (
        member.otp_codes.filter(used_at__isnull=True, expires_at__gt=timezone.now())
        .order_by("-created_at")
        .first()
    )
    if otp is None:
        raise OtpError(_("Aucun code valide. Demandez un nouveau SMS."))

    otp.attempts += 1
    otp.save(update_fields=["attempts"])
    if otp.attempts > OTP_MAX_ATTEMPTS:
        raise OtpError(_("Trop de tentatives. Demandez un nouveau code."))

    if not check_password((raw_code or "").strip(), otp.code_hash):
        raise OtpError(_("Code incorrect."))

    otp.used_at = timezone.now()
    otp.save(update_fields=["used_at"])
    member.phone_verified = True
    member.save(update_fields=["phone_verified"])
    return True
