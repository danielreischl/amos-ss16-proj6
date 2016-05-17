from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^position.csv', views.db2csv, name='position'),
]
