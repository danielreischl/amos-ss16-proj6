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


# This class tests if all necessary folders exist
class TestFolderExistence (unittest.TestCase):

    # Folder InitialData
    def testFolderInitialData(self):
        res = True
        self.assertEqual(res, os.path.isdir("srv/DataProcessing/InitialData"))

    # Folder InitialDataArchive
    def testFolderInitialDataArchive(self):
        res = True
        self.assertEqual(res, os.path.isdir("srv/DataProcessing/InitialDataArchive"))

    # Folder CarrierData
    def testFolderCarrierData(self):
        res = True
        self.assertEqual(res, os.path.isdir("srv/DataProcessing/CarrierData"))

    # Folder CarrierDataArchive
    def testFolderCarrierDataArchive(self):
        res = True
        self.assertEqual(res, os.path.isdir('srv/DataProcessing/CarrierDataArchive'))

    if __name__ == '__main__':
        unittest.main()