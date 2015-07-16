from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'media_explorer_example.views.home', name='home'),
    # url(r'^media_explorer_example/', include('media_explorer_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Disable password change
    url(r'^admin/password_change/', 'blog.views.index'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    ("^ckeditor/", include("ckeditor.urls")),
    ("^", include("media_explorer.urls")),

    url(r'^$', 'blog.views.index'),
    url(r'^(?P<slug>[\w\-]+)/$', 'blog.views.post'),   

)
