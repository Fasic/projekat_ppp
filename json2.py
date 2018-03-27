import json
from urllib.parse import urlparse, parse_qs
"""x = []
for i in range(10):
    a = ["asd asd"]
    for j in range(15):
        a.append(0)
    x.append(a)
data = {}
data['prisutni'] = x
json_data = json.dumps(data)

print(json_data)


url = "ime=dfgdfgdfg&prezime=dfgdfg&brIndeksa=&ime=WEB+Dizajn"
post_data = parse_qs(urlparse("?" + url).query)
print(post_data["prezime"][0])"""


import sqlite3
conn = sqlite3.connect('baza.db')
c = conn.cursor()

for i in range(1,0):
    c.execute("INSERT INTO termin (broj, aktivan, idPredmeta) VALUES ("+str(i)+", 0, 2)")


c.execute('SELECT * FROM termin WHERE broj=14')
print(c.fetchone()[0])

conn.commit()
conn.close()
