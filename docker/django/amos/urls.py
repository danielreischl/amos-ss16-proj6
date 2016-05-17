from django.conf.urls import include, url
from helloWorld import views
from django.contrib import admin

urlpatterns = [
    url(r'^django/helloWorld/', include('helloWorld.urls')),
    # the following is a hack; try to improve
    url(r'^django/index.html', include('helloWorld.urls')),
    url(r'^django/admin/', admin.site.urls),
]
