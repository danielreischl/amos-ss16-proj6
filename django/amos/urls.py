from django.conf.urls import include, url
from helloWorld import views
#from django.contrib import admin

urlpatterns = [
    url('helloWorld/', include('helloWorld.urls')),
    # the following is a hack; try to improve
    url('index.html', include('helloWorld.urls')),
    #url(r'^admin/', admin.site.urls),
]
