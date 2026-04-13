# foodiehub/context_processors.py
from .translations import TRANSLATIONS, get_translation

def language(request):
    lang = getattr(request, 'lang', request.session.get('lang', 'en'))
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    return {
        'LANG': lang,
        'T': trans,
    }
