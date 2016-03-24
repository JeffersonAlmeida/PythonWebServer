from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverhandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            messagecontent = ""
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent += fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass

    def do_GET(self):
        try:
            if self.path.endswith("/menus"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rest_collection = session.query(MenuItem).all()
                output = ""
                output += "<ul>"
                output += "<html><body>"
                for r in rest_collection:
                    output += r.name
                    output += "</br>"
                    output += "<a href=#''>Edit</a></br>"
                    output += "<a href=#''>Delete</a></br>"
                    output += "</br></br>"

                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rest_collection = session.query(Restaurant).all()
                output = ""
                output += "<ul>"
                output += "<html><body>"
                for r in rest_collection:
                    output += r.name
                    output += "</br>"
                    output += "<a href=#''>Edit</a></br>"
                    output += "<a href=#''>Delete</a></br>"
                    output += "</br></br>"

                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rest_collection = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<h1> Make a New Restaurant </h1>"
                output += "<input type='text' name='name'>"
                output += "<input type='submit' value='Create'>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

        try:
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def main():
    try:
        server_name = ''
        server_port = 8080
        server = HTTPServer((server_name, server_port), webserverhandler)
        print "Web Server Running on Port %s" %server_port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Ctrl + C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
