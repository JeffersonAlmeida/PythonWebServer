from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
import cgi
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverhandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant_object = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if restaurant_object :
                    session.delete(restaurant_object)
                    session.commit()
                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/restaurants')

            if self.path.endswith("/hola"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hola'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurant')
                    newRest = Restaurant()
                    newRest.name = messagecontent[0]
                    print newRest.name
                    session.add(newRest)
                    session.commit()
                    print newRest.name
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updateRestaurant')
                    restaurant_id = self.path.split("/")[2]
                    restaurant_object = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    if restaurant_object != [] :
                        restaurant_object.name = messagecontent[0]
                        session.add(restaurant_object)
                        session.commit()
                        self.send_response(301)
                        self.send_header('content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
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

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                print "sim"
                rest_collection = session.query(Restaurant).all()
                if rest_collection:
                    print "sim"
                else:
                    print "nao"

                output = ""
                output  += "<a href='/restaurants/new'> Create a new Restaurant Here </a></br></br>"
                output += "<ul>"
                output += "<html><body>"
                for r in rest_collection:
                    output += r.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a></br>" % r.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a></br>" % r.id
                    output += "</br></br>"

                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                restaurant_object = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if restaurant_object:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += restaurant_object.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant_id
                    output += "<input type='text' name='updateRestaurant' placeholder='%s'>" % restaurant_object.name
                    output += "<input type='submit' value='Update'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant_object = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if restaurant_object:
                    self.send_response(200)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += "Are you sure you want to delete: </br> %s " % restaurant_object.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant_id
                    output += "<input type='submit' name='updateRestaurant' value='Delete'></form>"
                    output += "<a href='/restaurants'>Back to Restaurants</a>"
                    output += "</body></html>"
                    print output
                    self.wfile.write(output)

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rest_collection = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<h2> Make a New Restaurant</h2>"
                output += "<input name='newRestaurant' type='text' >"
                output += "<input type='submit' value='Create'></form>"
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
                output += '''<form method='POST' enctype='multipart/form-data' action='/hola'><h2>What would you like me to say?</h2>
                <input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except:
            self.send_error(404, 'File Not Found: %s' % self.path)

def main():
    try:
        server_name = ''
        server_port = 5000
        server = HTTPServer((server_name, server_port), webserverhandler)
        print "Web Server Running on Port %s" %server_port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Ctrl + C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
