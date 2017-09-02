from django.conf.urls import include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='game:login', permanent=True), name='login'),
    url(r'^game/', include('game.urls', namespace='game')),
    url(r'^admin/', include(admin.site.urls)),
]
