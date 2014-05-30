from django.conf import settings
from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', 'pet_chooser.views.witch_journey', name='home'),
    url(r'^finished/$', 'pet_chooser.views.finished_journey', name='finished'),
    url(r'^f/(?P<form_name>.+)/$', 'pet_chooser.views.witch_journey', name='named_form'),
    # url(r'^witchform/', include('witchform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^favicon.ico$', 'django.views.static.serve', {'document_root': 'static/'}),
    )
