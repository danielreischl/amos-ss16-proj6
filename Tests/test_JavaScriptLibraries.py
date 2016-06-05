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

# Tests if all in index.html defined libraries are also installed on the server.

import os
# To run the unittests
import unittest
# to Parse the html file
from HTMLParser import HTMLParser
# To read a html file
import codecs


# Creates a suubclass of the HTMLParser to override the settings
class checkScriptLoadParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # if start tag is script, add the attributes to allScriptAttributes
        if tag == 'script':
            allScriptAttributes.append(attrs)

# Creates a list to store all script attributes
allScriptAttributes = []

# Path of Static Files
PATH_OF_STATIC_FILES = '/srv/static/'

# Instantiates the parser and feeds it with the index.html file
parser = checkScriptLoadParser()
indexFile = codecs.open(PATH_OF_STATIC_FILES + "index.html", 'r')
parser.feed(indexFile.read())

# Defines the test
class TestSequense (unittest.TestCase):
    pass

def test_allLibPath(path):
    def doTest(self):
        res = True
        self.assertEqual (res, os.path.exists(path))
    return doTest

if __name__ == '__main__':
    # for each attribute in allScriptAttributes the test is called
    for reference in allScriptAttributes:
        # Removes ' out of the reference
        reference = str(reference[0]).split(',')[1]
        reference = reference[2:len(reference)-2]
        # Names the testcase
        test_name = 'test_%s' % reference
        # Defines the test
        test=test_allLibPath(PATH_OF_STATIC_FILES + reference)
        # Sets the attributes
        setattr(TestSequense, test_name, test)
    unittest.main()