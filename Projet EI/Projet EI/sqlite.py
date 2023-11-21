import sqlite3, re


concord = open('corpus-medical_snt/concord.html','r')
res = re.findall(r'<a href=\"[0-9 ]+\">.+</a>',concord.read())

for i in range(len(res)):
    res[i] = re.findall(r'>.+<',res[i])[0][1:-1]

con= sqlite3.connect("extraction.db")
con.execute("CREATE TABLE POSOLOGIE(id INTEGER , posologie TEXT)")
i=1

for line in res:
     print(str(i)+'\t'+line)
     con.execute("INSERT INTO POSOLOGIE VALUES (?,?)",(str(i),line))
     i=i+1



 
con.commit()
