f = open('helloworld1.html','w')

message = """<html>
<head></head>
<body>
<p>Hello World!</p>
</body>
</html>"""

f.write(message)
f.close()
