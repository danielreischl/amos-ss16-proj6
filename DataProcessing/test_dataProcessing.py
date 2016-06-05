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

# This files includes all tests for dataProcessing
import unittest
import os
import setConstants


# This class tests if all necessary folders exist
class testFolderExistence (unittest.TestCase):

    # Folder InitialData
    def test_FolderInitialData(self):
        res = True
        self.assertEqual(res, os.path.isdir("/srv/DataProcessing/InitialData"))

    # Folder InitialDataArchive
    def test_FolderInitialDataArchive(self):
        res = True
        self.assertEqual(res, os.path.isdir("/srv/DataProcessing/InitialDataArchive"))

    # Folder CarrierData
    def test_FolderCarrierData(self):
        res = True
        self.assertEqual(res, os.path.isdir("/srv/DataProcessing/CarrierData"))

    # Folder CarrierDataArchive
    def test_FolderCarrierDataArchive(self):
        res = True
        self.assertEqual(res, os.path.isdir('/srv/DataProcessing/CarrierDataArchive'))

# Checks if all files are existing
class testFileExistence (unittest.TestCase):

    # compressInitialData.py
    def test_CompressIntitialData (self):
        res = True
        self.assertEqual (res, os.path.exists('/srv/DataProcessing/compressInitialData.py'))

    # writeCarrierDataToDataBase
    def test_WriteDataToDatabase(self):
        res = True
        self.assertEqual(res, os.path.exists('/srv/DataProcessing/writeCarrierDataToDataBase.py'))

    # setConstants.py
    def test_SetConstants(self):
        res = True
        self.assertEqual(res, os.path.exists('/srv/DataProcessing/setConstants.py'))

    # sqliteDB
    def test_DataBaseFile(self):
        res = True
        self.assertEqual(res, os.path.exists(setConstants.PATH_OF_SQLLITE_DB))

if __name__ == '__main__':
    unittest.main()