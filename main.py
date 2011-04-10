#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class MainHandler(webapp.RequestHandler):
    def get(self):
        head = """<title>Tamarindo</title>"""
        body = """<form action="." method="post"><input type="text" name="title"><input type="submit" value="Add"></form>"""
        page = """<html><head>%s</head><body>%s</body></html>""" % (head, body)
        self.response.out.write(page)


def main():
    application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
