from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^csv.request', views.db2csv, name='position'),

    # Added the url values to enable the frontend to request values like LastItteratioOfaCarrier
    # Calls views.db2values (Further Information views.py)
    url(r'^values.request', views.db2values, name='values'),
]
