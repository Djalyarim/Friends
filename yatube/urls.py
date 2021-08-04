from django.conf import settings
# from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.staticfiles.urls import \
#     staticfiles_urlpatterns  # for ngrok
from django.urls import include, path, re_path
from django.views.static import serve  # for ngrok
from rest_framework.authtoken import views
from django.views.generic import TemplateView

handler404 = 'posts.views.page_not_found'  # noqa
handler500 = 'posts.views.server_error'  # noqa

urlpatterns = [
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

urlpatterns += re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # for ngrok
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]  # for ngrok
# urlpatterns += [path('api-token-auth/', views.obtain_auth_token)]
