from django.utils.translation.trans_real import *
from django.utils.translation import trans_real

TO_FULL = {
    'br': 'pt_BR',
    'cn': 'zh_CN',
}

_accepted = {}
def get_language_from_request(request, check_path=False):
    """
    Analyzes the request to find what language the user wants the system to
    show. Only languages listed in settings.LANGUAGES are taken into account.
    If the user requests a sublanguage where we have a main language, we send
    out the main language.

    If check_path is True, the URL path prefix will be checked for a language
    code, otherwise this is skipped for backwards compatibility.
    """
    global _accepted
    from django.conf import settings
    supported = dict(settings.LANGUAGES)

    lang_code = request.META.get('HTTP_HOST', 'dolphin-emu.org').split('.')[0]

    full_lang_code = TO_FULL.get(lang_code, lang_code)
    if lang_code and lang_code in supported and check_for_language(full_lang_code):
        return full_lang_code

    return settings.LANGUAGE_CODE

trans_real.get_language_from_request = get_language_from_request
