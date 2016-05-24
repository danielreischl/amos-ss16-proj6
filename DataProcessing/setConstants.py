#!/usr/bin/env python

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

# File to maintain all constants which will be used in all DataProcessing Scripts

# Length of one Drive
DRIVE_LENGTH = 4
# Length of all drives
LINE_LENGTH = 12
# Amount of Carriers
AMOUNT_OF_CARRIERS = 15
# Wait time of the Simulator in Seconds used in compressInitialData.py
WAIT_TIME_IN_SECONDS_DPPY = 0.001
#Session of the demonstrator setting
SESSION = 1
# WaitTime of writeCarrierDataToDataBase.py
WAIT_TIME_IN_SECONDS_MPY = 5
# Separator of the CSV-Files
CSV_SEPARATOR = ";"

# Path of SQLITEDB
PATH_OF_SQLLITE_DB = '/srv/django/db.sqlite3'

NAME_TABLE_PROCESSED_DATA = 'helloWorld_timestampdata'
NAME_TABLE_COM_DATA = 'helloWorld_iterationdata'

NAME_TABLE_CARRIER = 'helloWorld_carrier'
NAME_TABLE_ITERATION = 'helloWorld_iteration'
NAME_TABLE_ITERATION = 'helloWorld_session'

