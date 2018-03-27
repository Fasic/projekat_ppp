import http.server
Server = http.server.HTTPServer
BaseHandler = http.server.BaseHTTPRequestHandler
import json
json.dumps(['select', 'asd'])


class Handler(BaseHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            putanja = self.path[1:]
            if(putanja == ""):
                putanja = "index.html"
                f = open(putanja) #open requested file
                self.wfile.write(str.encode(f.read()))
            if(putanja == "registracija"):
                print("registracija")
                putanja = "registracija.html"
                f = open(putanja) #open requested file
                self.wfile.write(str.encode(f.read()))
            if(putanja == "prisustvo"):
                print("Prisustvo")
                self.wfile.write(str.encode("Fasic")) #ide return tabelu sa prisutnima!!!
            if(putanja == "imena"):
                print("Imena")
                s = "{\"select\":[\"Filip Vasic\",\"Dragan Dragan\"]}"
                print(s)
                self.wfile.write(str.encode(s)) #ide return tabelu sa prisutnima!!!
                        
                
            

        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            # Print posted data
            putanja = self.path.split("/")
            x = putanja[1]
            if(x == "prijavljivanje"): print("Prijavljivanje")
            elif(x == "registracija"): print("Registracija")
            else: print("Error 404 page not found.")


            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(content_length)
            print (post_data)
            self._set_headers()
            html = "<html><body><h1>POST!</h1><pre>" + str(post_data.decode("utf-8")) + "</pre></body></html>"
            self.wfile.write(str.encode(html))


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
