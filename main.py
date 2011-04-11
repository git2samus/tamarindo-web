#!/usr/bin/env python
import cgi, urllib

from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import util

class Node(db.Model):
    title = db.StringProperty()
    associations = db.ListProperty(db.Key)


class MainHandler(webapp.RequestHandler):
    def get(self):
        nodes = Node.all()
        sorted_nodes = sorted(nodes, key=lambda node: node.title)

        head = """<title>Tamarindo</title>"""
        lcol = """<form action="." method="post"><input type="text" name="title"><input type="submit" value="Add"></form>""" + \
               """<form action="." method="post">%s -> %s <input type="submit" value="Connect"></form>""" % (
            """<select name="assoc_from"><option>---</option>%s</select>""" % ''.join(
                """<option value="%d">%s</option>""" % (node.key().id(), node.title) for node in sorted_nodes
            ),
            """<select name="assoc_to"><option>---</option>%s</select>""" % ''.join(
                """<option value="%d">%s</option>""" % (node.key().id(), node.title) for node in sorted_nodes
            ),
        ) + \
               """<ul>%s</ul>""" % ''.join(
            """<li><a href="#%d">%s</a></li>""" % (node.key().id(), node.title) for node in sorted_nodes
        )
        rcol = """<img src="http://chart.googleapis.com/chart?cht=gv&amp;chl=digraph{%s}">""" % urllib.quote(
            ','.join("\"%s\"" % node.title.replace("\\", "\\\\").replace("\"", "\\\"") for node in nodes)
        )
        body = """<table><tr><td>%s</td><td>%s</td></tr></table>""" % (lcol, rcol)
        page = """<html><head>%s</head><body>%s</body></html>""" % (head, body)

        self.response.out.write(page)

    def post(self):
        title = self.request.get('title')
        assoc_from, assoc_to = self.request.get('assoc_from'), self.request.get('assoc_to')

        if title:
            node = Node()
            node.title = cgi.escape(title)
            node.put()
        elif assoc_from and assoc_to and assoc_from.isdigit() and assoc_to.isdigit():
            node_from, node_to = Node.get_by_id(long(assoc_from)), Node.get_by_id(long(assoc_to))
            if node_from and node_to:
                node_from.associations.append(node_to.key())
                node_from.put()

        self.redirect('/')


def main():
    application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
