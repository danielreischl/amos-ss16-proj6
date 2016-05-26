#   This file is part of Rogue Vision.
#
#   Copyright (C) 2016 Daniel Reischl, Rene Rathmann, Peter Tan,
#       Tobias Dorsch, Shefali Shukla, Vignesh Govindarajulu,
#       Aleksander Penew, Abinav Puri
#
#   ReqTracker is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   ReqTracker is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PUROSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with rogueVision.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url

from . import views

urlpatterns = [
    # this returns a csv-file of the requested data - for details see views.py 
    url(r'^data.csv', views.db2csv, name='data'),
    # this returns a csv-file of raw database tables - for details see views.py 
    url(r'^rawData.csv', views.rawData, name='rawData'),
    # This returns the DataProcessing Logfile
    url(r'^log.txt', views.logs, name='DataProcessingLog'),
    # Added the url values to enable the frontend to request values like LastItteratioOfaCarrier
    # Calls views.db2values (Further Information views.py)
    url(r'^values.request', views.db2values, name='values'),


]
