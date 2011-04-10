#!/usr/bin/env python
import cgi, urllib

from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import util

class Node(db.Model):
    title = db.StringProperty()


class MainHandler(webapp.RequestHandler):
    def get(self):
        nodes = Node.all()
        node_string = ','.join("\"%s\"" % node.title.replace("\\", "\\\\").replace("\"", "\\\"") for node in nodes)

        head = """<title>Tamarindo</title>"""
        lcol = """<form action="." method="post"><input type="text" name="title"><input type="submit" value="Add"></form>""" + \
               """<ul>%s</ul>""" % ''.join("<li>%s</li>" % node.title for node in nodes)
        rcol = """<img src="http://chart.googleapis.com/chart?cht=gv&amp;chl=digraph{%s}">""" % urllib.quote(node_string)
        body = """<table><tr><td>%s</td><td>%s</td></tr></table>""" % (lcol, rcol)
        page = """<html><head>%s</head><body>%s</body></html>""" % (head, body)

        self.response.out.write(page)

    def post(self):
        node = Node()
        node.title = cgi.escape(self.request.get('title'))
        node.put()

        self.redirect('/')


def main():
    application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
