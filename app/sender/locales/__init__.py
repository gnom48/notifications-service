import os
import gettext
from typing import Callable
import logging

AVAILABLE_LANGUAGES = ['ru_RU', 'en_US']
DEFAULT_LANGUAGE = 'ru_RU'


def translation(lang: str | None = None) -> Callable[[str], str]:
    """
    Возвращает объект перевода для выбранного языка.
    """
    lang = lang or DEFAULT_LANGUAGE
    if lang not in AVAILABLE_LANGUAGES:
        logging.warning(
            f'Not supporting language "{lang}"; using default language')
        lang = DEFAULT_LANGUAGE

    localedir = os.path.join(os.path.dirname(__file__), 'locales')

    try:
        translator = gettext.translation(
            domain='messages',
            localedir=localedir,
            languages=[lang]
        )
        return translator.gettext
    except FileNotFoundError:
        logging.warning(
            f'No translation available for language "{lang}"; using default language')
        return lambda text: text


def try_get_translation(msg_id: str, lang: str | None = None) -> str:
    return translation(lang)(msg_id)
