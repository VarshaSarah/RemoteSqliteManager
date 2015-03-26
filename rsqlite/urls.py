from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', "system.views.login"),
    url(r'^search/$', "system.views.validatesearch"),
    url(r'^gotpath/(?P<anystring>.+)/$', "system.views.copy", name='vsearching'),
    url(r'^execute/$', "system.views.execute"),
    url(r'^commit/$', "system.views.commit"),
    url(r'^rollback/$', "system.views.rollback"),
    url(r'^hello/$', "system.views.hello"),
)
