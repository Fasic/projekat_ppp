import http.server
from urllib.parse import urlparse, parse_qs
import json
import sqlite3

Server = http.server.HTTPServer
BaseHandler = http.server.BaseHTTPRequestHandler
prviPut = 1
ajaxZahtevi = ["imena", "prisutni", "predmeti"]

class Handler(BaseHandler):
        def log_message(self, format, *args):
                return

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            #self._set_headers()
            putanja = self.path[1:]
            if(putanja == ""):
                putanja = "index"
                self.redirect(putanja + ".html")
            if(putanja == "registracija" or putanja == "prisustvo"):  self.redirect(putanja + ".html")


            #ajax zahtevi -------------------------------------------------------------
            if(putanja == "imena"): s = self.getImena()
            if(putanja == "predmeti"): s = self.getPredmete()
            if(putanja == "prisutni"):
                global prviPut
                prviPut+=1
                print("prisutni")
                s = self.fakeJsonPrisustvo()
                print(s)

            
            if(putanja in ajaxZahtevi):
                    self._set_headers()
                    self.wfile.write(str.encode(s))
                
            #ajax zahtevi -------------------------------------------------------------

        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            # Print posted data
            putanja = self.path.split("/")
            x = putanja[1]
            if(x == "prijavljivanje"):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                x = self.parsirajPOST(post_data)
                if("ime" not in x or "indeks" not in x): self.redirectPoruka("Neuspesna prijava! (Nisu popunjena sva polja)")
                else:
                        d = self.prijaviStudenta(x)
                        if(d == False): self.redirectPoruka("Neuspesna prijava! (Nema takvog studenta)")
                        else: self.redirectPoruka(d)

            elif(x == "registracija"):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                x = self.parsirajPOST(post_data)
                if("ime" not in x or "brIndeksa" not in x or "prezime" not in x or "predmet" not in x): self.redirectPoruka("Neuspesna registracija! (Nisu popunjena sva polja)")
                else:
                        d = self.registrujStudenta(x)
                        #if neuspesna registracija neuspesnaregistracija.html
                        if(d == False):  self.redirectPoruka("Neuspesna registracija!!! (Student vec postoji sudent)")
                        else: self.redirectPoruka("Uspesna registracija (" + d + ")")
                        

            else:
                poruka = "Error 404 page not found."
                print(poruka)
                self.wfile.write(str.encode(poruka))

        def parsirajPOST(self, post_data):
                url = str(post_data.decode("utf-8"))
                post_data = parse_qs(urlparse("?" + url).query)
                print(post_data)
                return post_data

        def redirect(self, putanja):
                self._set_headers()
                print("Redirect -->" + putanja)
                f = open(putanja)
                self.wfile.write(str.encode(f.read()))

        def redirectPoruka(self, poruka):
                self._set_headers()
                s1 = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Uspesna registracija</title>"""
                s2 = """</head><body>"""+ poruka + " (redirect za 5 sekundi!)" +"""</body></html>"""
                f = open("redirect.js")
                s = f.read()
                print(s1+s+s2)
                self.wfile.write(str.encode(s1+s+s2))
                

        def registrujStudenta(self, data):
                r = False
                ime = data["ime"][0].title()
                prezime = data["prezime"][0].title()
                indeks = data["brIndeksa"][0].upper()
                predmet = data["predmet"][0]


                
                idPredmeta = self.getIdPredmeta(predmet)


                conn = sqlite3.connect('baza.db')
                c = conn.cursor()
                poziv = 'SELECT * FROM student WHERE ime="'+ime+'" AND prezime="'+prezime+'" AND indeks="'+indeks+'" AND idPredmeta='+str(idPredmeta)
                #da bude samo indeks i predmet isto!

                c.execute(poziv)
                q = len(c.fetchall())
                if(q == 0):
                   insertPoziv = "INSERT INTO student (ime, prezime, indeks, idPredmeta) VALUES ('"+ime+"','"+prezime+"', '"+indeks+"','"+str(idPredmeta)+"')"
                   c.execute(insertPoziv)
                   conn.commit()
                   r = ime + " " + prezime
                else:
                   r = False


                conn.close()
                return r

        def prijaviStudenta(self, data):
                a = data["ime"][0].split(" ")
                ime = a[0]
                prezime = a[1]
                indeks = data["brIndeksa"][0].upper()
                indeks = indeks.upper()
                conn = sqlite3.connect('baza.db')
                c = conn.cursor()
                poziv = 'SELECT * FROM termin WHERE aktivan=1'
                c.execute(poziv)
                trenutno = c.fetchone()
                ID = trenutno[0]
                idPredmeta = trenutno[3]

                poziv = 'SELECT * FROM student WHERE ime="'+ime+'" AND prezime="'+prezime+'" AND indeks="'+indeks+'"'
                c.execute(poziv)
                w = c.fetchall()
                q = len(w)
                if(q == 0):
                        conn.close()
                        print("Nema studenta")
                        return False

                c.execute("SELECT * FROM prisustvo WHERE idPredmeta=" + str(idPredmeta) + " AND idStudenta=" + str(w[0][0]) + " AND  termin =" + str(ID))
                if(len(c.fetchall()) > 0):
                        conn.close()
                        return "Vec ste prijavljeni (" + ime + " " + prezime + ")"

                
                insertPoziv = "INSERT INTO prisustvo (idPredmeta, idStudenta, termin) VALUES (" + str(idPredmeta) + ", " + str(w[0][0]) + "," + str(ID) + ")"
                c.execute(insertPoziv)
                conn.commit()
                conn.close()
                return "Uspesna prijava (" + ime + " " + prezime + ")"
        
        def getIdPredmeta(self, naziv):
                conn = sqlite3.connect('baza.db')
                c = conn.cursor()
                poziv = 'SELECT * FROM predmet WHERE naziv="' + naziv + '"'
                c.execute(poziv)
                ret = c.fetchone()[0]
                conn.close()
                return ret


        def getImena(self):
                conn = sqlite3.connect('baza.db')
                c = conn.cursor()
                poziv = 'SELECT * FROM termin WHERE aktivan=1'
                c.execute(poziv)
                trenutno = c.fetchone()
                ID = trenutno[0]
                idPredmeta = trenutno[3]

                poziv = "SELECT * FROM student WHERE idPredmeta=" + str(idPredmeta) + " AND id not in (SELECT idStudenta FROM prisustvo WHERE termin=" + str(ID) + ")"
                c.execute(poziv)
                sviStudentiNaPredmetu = c.fetchall()

                x = []
                for i in sviStudentiNaPredmetu:
                    a = i[1] + " " + i[2]
                    x.append(a)
                data = {}
                data['select'] = x
                json_data = json.dumps(data)
                conn.close()
                return json_data
        
        def getPredmete(self):
                conn = sqlite3.connect('baza.db')
                c = conn.cursor()
                poziv = 'SELECT * FROM predmet'
                c.execute(poziv)
                trenutno = c.fetchall()
                x = []
                for i in trenutno:
                    a = i[1]
                    x.append(a)
                data = {}
                data['select'] = x
                json_data = json.dumps(data)
                conn.close()
                return json_data

            
        def fakeJsonPrisustvo(self):
                conn = sqlite3.connect('baza.db')
                c = conn.cursor()
                poziv = 'SELECT * FROM termin WHERE aktivan=1'
                c.execute(poziv)
                trenutno = c.fetchone()#ako nema aktivnih termina, ide za sve predmete ili se biraju predmeti xD
                ID = trenutno[0]
                idPredmeta = trenutno[3]

                upit = "SELECT s.ime, s.prezime, s.id FROM prisustvo INNER JOIN student as s on prisustvo.idStudenta = s.id WHERE prisustvo.termin=" + str(ID)
                c.execute(upit)
                sviStudentiNaPredmetu = c.fetchall()

                x = []
                for i in sviStudentiNaPredmetu:

                    prisustva = "SELECT broj FROM prisustvo as p INNER JOIN termin as t ON p.termin = t.id WHERE p.idStudenta = " + str(i[2])
                    c.execute(prisustva)
                    z = c.fetchall()
                    

                    print(z)
                    a = [str(i[0]) + " " + str(i[1])]
                    for j in range(1,16):
                        if((j,) in z): a.append(1)
                        else: a.append(0)
                    x.append(a)
                data = {}
                data['prisutni'] = x
                json_data = json.dumps(data)
                conn.close()
                return json_data



def run(server_class=Server, handler_class=Handler, port=8888):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        
        print ('Starting httpd...')
        httpd.serve_forever()

if __name__ == "__main__":
        from sys import argv

        if len(argv) == 2:
            run(port=int(argv[1]))
        else:
            run()
