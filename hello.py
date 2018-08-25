import sqlite3
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import cgi
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'success': True}).encode())
        return
    
this_is_python = True

if this_is_python:
    print("welcome to python!")
    

conn = sqlite3.connect('example.db')

c = conn.cursor()

c.execute('''drop table users''')
c.execute('''create table users (username text, password text)''')
c.execute("""insert into users values ('nsp', 'apkdo')""")
conn.commit()
c.close()

httpd = HTTPServer(('0.0.0.0', 8000), RequestHandler)

while True:
    httpd.handle_request()
    
