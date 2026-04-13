# Add this as foodiehub/language_middleware.py

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.session.get('lang', 'en')
        if lang not in ['en', 'te', 'hi']:
            lang = 'en'
        request.lang = lang
        response = self.get_response(request)
        return response


# Add this view to restaurants/views.py or accounts/views.py
def set_language(request):
    from django.shortcuts import redirect
    lang = request.POST.get('lang', 'en')
    if lang in ['en', 'te', 'hi']:
        request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))
