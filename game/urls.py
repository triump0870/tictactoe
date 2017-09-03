from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^play/$', views.index, name='play'),
    url(r'^(?P<pk>\d+)/$', views.game, name='detail'),
    url(r'^$', views.login, name='login')
]
