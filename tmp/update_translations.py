"""Merge English translations into django.po and compile django.mo."""
from pathlib import Path
import polib

PO_PATH = Path(__file__).resolve().parents[1] / "locale" / "en" / "LC_MESSAGES" / "django.po"
MO_PATH = PO_PATH.with_suffix(".mo")

TRANSLATIONS = {
    "Forum": "Forum",
    "Contact": "Contact",
    "Menu": "Menu",
    "Action PNAC": "PNAC Action",
    "Voir toutes les actions": "See all actions",
    "Qui sommes-nous (Mission)": "Who we are (Mission)",
    "Partenariats multi-partites": "Multi-stakeholder partnerships",
    "Non disponible": "Unavailable",
    "Aucun événement prévu pour le moment.": "No events scheduled at the moment.",
    "Zone d'intervention prioritaire": "Priority intervention area",
    "Voir détails": "View details",
    "Redirection vers MaxiCash...": "Redirecting to MaxiCash...",
    "Numéro de Téléphone": "Phone number",
    "PNAC - RDC | Partenariat Novateur pour l'Assainissement Communautaire": (
        "PNAC - DRC | Innovative Partnership for Community Sanitation"
    ),
    "PNAC - Programme Novateur pour l'Assainissement Communautaire": (
        "PNAC - Innovative Program for Community Sanitation"
    ),
    # Privacy policy
    "Politique de Confidentialité": "Privacy Policy",
    "Votre vie privée est importante pour nous. Découvrez comment le PNAC protège et utilise vos informations.": (
        "Your privacy matters to us. Learn how PNAC protects and uses your information."
    ),
    "Introduction": "Introduction",
    "Le Programme Novateur pour l'Assainissement Communautaire (PNAC) s'engage à protéger la confidentialité des utilisateurs de son site web. Cette politique de confidentialité explique quelles informations nous recueillons, comment nous les utilisons et comment nous les protégeons.": (
        "The Innovative Community Sanitation Program (PNAC) is committed to protecting the privacy of its website users. This privacy policy explains what information we collect, how we use it, and how we protect it."
    ),
    "Collecte des Informations": "Information Collection",
    "Nous pouvons collecter les types d'informations suivants :": (
        "We may collect the following types of information:"
    ),
    "Informations personnelles": "Personal information",
    "Nom, adresse e-mail, numéro de téléphone, et autres coordonnées que vous nous fournissez volontairement lors de l'inscription à notre newsletter, de l'utilisation de nos formulaires de contact ou lors de la participation à nos forums.": (
        "Name, email address, phone number, and other contact details that you voluntarily provide when signing up for our newsletter, using our contact forms, or participating in our forums."
    ),
    "Informations non personnelles": "Non-personal information",
    "Données de navigation, type de navigateur, adresse IP, et pages visitées sur notre site, collectées via des cookies et des outils d'analyse.": (
        "Browsing data, browser type, IP address, and pages visited on our site, collected via cookies and analytics tools."
    ),
    "Utilisation des Informations": "Use of Information",
    "Les informations collectées sont utilisées pour :": "The information collected is used to:",
    "Vous fournir les services demandés et répondre à vos questions.": (
        "Provide the requested services and answer your questions."
    ),
    "Améliorer le contenu et la fonctionnalité de notre site web.": (
        "Improve the content and functionality of our website."
    ),
    "Vous envoyer des newsletters, des mises à jour sur nos projets et des appels à l'action (vous pouvez vous désinscrire à tout moment).": (
        "Send you newsletters, project updates, and calls to action (you may unsubscribe at any time)."
    ),
    "Analyser les tendances d'utilisation pour optimiser notre impact.": (
        "Analyze usage trends to optimize our impact."
    ),
    "Protection des Données": "Data Protection",
    "Nous mettons en œuvre des mesures de sécurité appropriées pour protéger vos informations contre l'accès non autorisé, la modification, la divulgation ou la destruction. Cependant, aucune transmission de données sur Internet n'est totalement sécurisée, et nous ne pouvons garantir une sécurité absolue.": (
        "We implement appropriate security measures to protect your information against unauthorized access, alteration, disclosure, or destruction. However, no data transmission over the Internet is completely secure, and we cannot guarantee absolute security."
    ),
    "Cookies": "Cookies",
    "Notre site utilise des cookies pour améliorer votre expérience utilisateur. Vous pouvez choisir de désactiver les cookies dans les paramètres de votre navigateur, mais cela pourrait affecter certaines fonctionnalités du site.": (
        "Our site uses cookies to improve your user experience. You can disable cookies in your browser settings, but this may affect some site features."
    ),
    "Vos Droits": "Your Rights",
    "Conformément à la législation en vigueur, vous disposez d'un droit d'accès, de rectification et de suppression de vos données personnelles. Pour exercer ce droit, veuillez nous contacter à l'adresse ci-dessous.": (
        "In accordance with applicable law, you have the right to access, correct, and delete your personal data. To exercise this right, please contact us at the address below."
    ),
    "Nous Contacter": "Contact Us",
    "Si vous avez des questions concernant cette politique de confidentialité, vous pouvez nous contacter à :": (
        "If you have questions about this privacy policy, you can contact us at:"
    ),
    "Dernière mise à jour :": "Last updated:",
    # Volunteer
    "Rejoignez l'Équipe PNAC": "Join the PNAC Team",
    "Devenez acteur du changement dans votre communauté. Ensemble, assainissons notre environnement.": (
        "Become an agent of change in your community. Together, let's clean up our environment."
    ),
    "Actions de terrain (Salongo)": "Field actions (Salongo)",
    "Sensibilisation citoyenne": "Citizen awareness",
    "Eco-brigades locales": "Local eco-brigades",
    "Suivez-nous sur les réseaux": "Follow us on social media",
    "Formulaire d'adhésion": "Membership form",
    "Nous vous enverrons une confirmation par ce canal.": (
        "We will send you a confirmation through this channel."
    ),
    "Envoyer ma candidature": "Submit my application",
    "Message de motivation": "Motivation message",
    "Mode de communication préféré": "Preferred communication method",
    "Votre nom complet": "Your full name",
    "Dites-nous pourquoi vous voulez rejoindre notre équipe...": (
        "Tell us why you want to join our team..."
    ),
    "Votre demande d'adhésion a été envoyée avec succès ! Nous vous contacterons bientôt.": (
        "Your membership request has been sent successfully! We will contact you soon."
    ),
    # Forum
    "Votre nom ou pseudo": "Your name or username",
    "Partagez votre avis ou signalez un problème...": (
        "Share your opinion or report a problem..."
    ),
    "Votre message a été publié avec succès !": "Your message has been published successfully!",
    # Models / choices
    "Formation & Sensibilisation": "Training & Awareness",
    "Guides & Sensibilisation": "Guides & Awareness",
    "Outils Salongo & Technique": "Salongo Tools & Technical Resources",
    "Documents Officiels": "Official Documents",
    "Français": "French",
    "English": "English",
    "Merci %(name)s ! Votre inscription pour « %(event)s » est enregistrée.": (
        'Thank you %(name)s! Your registration for "%(event)s" has been recorded.'
    ),
}

PYTHON_FORMAT = {
    "Merci %(name)s ! Votre inscription pour « %(event)s » est enregistrée.",
}


def main():
    po = polib.pofile(str(PO_PATH))
    po.metadata["Language"] = "en"
    po.metadata["Last-Translator"] = "PNAC <info@pnac-rdc.org>"

    for entry in po:
        if entry.msgid == "":
            entry.flags = [flag for flag in entry.flags if flag != "fuzzy"]

    existing = {entry.msgid: entry for entry in po}

    added = 0
    filled = 0
    for msgid, msgstr in TRANSLATIONS.items():
        entry = existing.get(msgid)
        if entry is None:
            flags = ["python-format"] if msgid in PYTHON_FORMAT else []
            po.append(polib.POEntry(msgid=msgid, msgstr=msgstr, flags=flags))
            added += 1
        else:
            if not entry.msgstr:
                entry.msgstr = msgstr
                filled += 1
            if msgid in PYTHON_FORMAT and "python-format" not in entry.flags:
                entry.flags.append("python-format")
            if "fuzzy" in entry.flags:
                entry.flags.remove("fuzzy")

    po.save(str(PO_PATH))
    po.save_as_mofile(str(MO_PATH))

    untranslated = [e.msgid for e in po.untranslated_entries() if e.msgid]
    print(f"Added {added} entries, filled {filled} empty msgstr.")
    print(f"Untranslated remaining: {len(untranslated)}")
    for msgid in untranslated[:40]:
        print(" -", msgid.replace("\n", " ")[:120])


if __name__ == "__main__":
    main()
