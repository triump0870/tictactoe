from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.conf import settings
from django.views import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='game:login', permanent=True), name='login'),
    url(r'^game/', include('game.urls', namespace='game')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += [
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}),
]