#@author: AMOUSus & Vick
#Codesnipet to explain how to access a MySQLDatabase by a Python Script

import MySQLdb

#Open Database Connection (Host, User, Passwort, Database)
db = MySQLdb.connect("localhost","admin","password","test" )

#Define Cursor
cursor = db.cursor()

#SQL Statement
sql = "Select * from testtable"

try:
    #Executes the Querry
    cursor.execute(sql)
    #Fetch the Results
    result = cursor.fetchall()
    #Print each row (Testdatabase has just one column)
    for row in result:
        print row[0]
except:
    print "Error"

#Close the connection
db.close
