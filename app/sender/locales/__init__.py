import os
import gettext

LOCALE_DIR = os.path.dirname(__file__)

AVAILABLE_LANGUAGES = ['ru_RU', 'en_US']
DEFAULT_LANGUAGE = 'ru_RU'


def translation(lang_code: str | None = None):
    lang_code = lang_code or DEFAULT_LANGUAGE
    translation = gettext.translation(
        domain='messages', localedir=LOCALE_DIR, languages=[lang_code])
    return translation.gettext
