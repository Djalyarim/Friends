import datetime as dt

from django.conf import settings


def year(request):
    year_now = dt.datetime.now().year
    return {'year': year_now}


def default_avatar(request):
    return {
        'default_avatar': settings.MEDIA_ROOT + 'users/default_avatar.png' 
    }
