#!/usr/bin/env python

#   This file is part of Rogue Vision.
#
#   Copyright (C) 2016 Daniel Reischl, Rene Rathmann, Peter Tan,
#       Tobias Dorsch, Shefali Shukla, Vignesh Govindarajulu,
#       Aleksander Penew, Abhinav Puri
#
#   Rogue Vision is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Rogue Vision is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with Rogue Vision.  If not, see <http://www.gnu.org/licenses/>.


# File to create a config file
import ConfigParser

# ToDO: Create the paths automatically

# Initializes a new Configparser
config = ConfigParser.RawConfigParser()

# Adds a section for paths
config.add_section('Paths')
# Adds path to database
config.set('Paths', 'database', '/srv/django/db.sqlite3')
# Adds path to root folder
config.set('Paths', 'root', '/srv/')
# Adds path to DataProcessing
config.set('Paths', 'dataProcessing', '/srv/DataProcessing')
# Adds path to InitialData
config.set('Paths', 'InitialData', '/srv/DataProcessing/InitialData')
# Adds path to InitialDataArchive
config.set('Paths', 'InitialDataArchive', '/srv/DataProcessing/InitialDataArchive')
# Adds path to CarrierData
config.set('Paths', 'CarrierData', '/srv/DataProcessing/CarrierData')
# Adds path to CarrierDataArchive
config.set('Paths', 'CarrierDataArchive', '/srv/DataProcessing/CarrierDataArchive')

# Adds Parameters of Simulation
config.add_section('Simulation')
# Adds Parameter for AmountOfCarriers
config.set('Simulation', 'Amount_Of_Carriers', 15)
# Adds Parameter for WaitTimeCompression
config.set('Simulation', 'WaitTime_Compression', 0.001)
# Adds Parameter for WaitTime_First_DataLoad
config.set('Simulation', 'WaitTime_First_DataLoad', 30)
# Adds Parameter for WaitTime_Data_Reload
config.set('Simulation', 'WaitTime_Data_Reload', 30)
# Adds Parameter for Session
config.set('Simulation', 'Session', 1)
# Adds CSV-Sperator
config.set('Simulation', 'csv_seperator', ';')
# Adds Keep Every X Rows
config.set('Simulation', 'keep_every_x_rows', 100)

# Adds database parameters
config.add_section("database_tables")
# Adds average table
config.set('database_tables', 'average', 'dataInterface_iterationdata')
# Adds continuous table
config.set('database_tables', 'continuous', 'dataInterface_timestampdata')

# Writes configuration as settings.cfg
with open('settings.cfg', 'wb') as configfile:
    config.write(configfile)