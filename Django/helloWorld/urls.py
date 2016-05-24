from django.conf.urls import url

from . import views

urlpatterns = [
    # this returns a csv-file of the requested data - for details see views.py 
    url(r'^data.csv', views.db2csv, name='data'),

    # Added the url values to enable the frontend to request values like LastItteratioOfaCarrier
    # Calls views.db2values (Further Information views.py)
    url(r'^values.request', views.db2values, name='values'),
]
