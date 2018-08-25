import sqlite3
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from datetime import datetime
import urllib.parse as urlparse
import cgi
import json

conn = sqlite3.connect('posts.db')
c = conn.cursor()
c.execute('''create table if not exists posts (created_at date, content text)''')
conn.commit()
c.close()

class Post(object):
    def __init__(self, content):
        self.content = content

def as_post(dct):
    if '__post__' in dct:
        return Post(dct['content'])
    return dct
        
def SelectAllPosts(conn):
    """
    Return all posts in the database
    """
    cur = conn.cursor()
    cur.execute('select created_at as "created_at [timestamp]", content from posts')
    rows = cur.fetchall()
    cur.close()
    return rows

class RequestHandler(BaseHTTPRequestHandler):

    def return_timeline(self):
        with open('./index.html', 'r') as webfile:
            web = webfile.read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(web.encode())
        return
    
    def do_GET(self):
        print(self.path)
        if self.path == '/posts':
            self.send_response(200)
            self.end_headers()
            # self.wfile.write(json.dumps({'posts': SelectAllPosts(conn)}).encode())
            for post in SelectAllPosts(conn):
                self.wfile.write('<div class="post">{0}</div><div class="date">{1}</div>'.format(post[0], post[1]).encode())
        else:
            self.return_timeline()
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'],})
        post = form['post']
        print(post.value)
        post_len = len(post.value)
        if post_len > 0 and post_len < 144:
            cur = conn.cursor()
            now = datetime.utcnow()
            cur.execute("insert into posts(created_at, content) values (?, ?)", (post.value, now))
            cur.close()
            self.return_timeline()
        else:
            self.send_response(400)
            self.end_headers()
        return

    def do_POST_OLD(self):
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        post = json.loads(post_body.decode("utf-8"), object_hook=as_post)
        print(post.content)
        post_len = len(post.content)
        if post_len > 0 and post_len < 144:
            cur = conn.cursor()
            now = datetime.utcnow()
            cur.execute("insert into posts(created_at, content) values (?, ?)", (post.content, now))
            cur.close()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({'success': False}).encode())
        return

httpd = HTTPServer(('0.0.0.0', 8000), RequestHandler)

while True:
    httpd.handle_request()
    
