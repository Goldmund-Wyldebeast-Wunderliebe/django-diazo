from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore

from django_diazo.models import Theme


def get_active_theme(request):
    if request.GET.get('theme', None):
        try:
            return Theme.objects.get(pk=request.GET.get('theme'))
        except Theme.DoesNotExist:
            pass
    for theme in Theme.objects.filter(enabled=True).order_by('sort'):
        if theme.available(request):
            return theme
    return None


def check_themes_enabled(request):
        """
        Check if themes are enabled for the current session/request.
        """
        if settings.DEBUG and request.GET.get('theme') == 'none':
            return False
        if 'sessionid' not in request.COOKIES:
            return True
        session = SessionStore(session_key=request.COOKIES['sessionid'])
        return session.get('django_diazo_theme_enabled', True)
