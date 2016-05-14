from django.conf.urls import include, url
from helloWorld import views
from django.contrib import admin

urlpatterns = [
    url('django/helloWorld/', include('helloWorld.urls')),
    # the following is a hack; try to improve
    url('django/index.html', include('helloWorld.urls')),
    url('django/admin/', include(admin.site.urls)),
]
