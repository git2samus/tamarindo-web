#!/usr/bin/env python
from google.appengine.dist import use_library
use_library('django', '1.2')

import urllib

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Node


class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            nodes = Node.all()
            nodes.order('title')

            nodes_dict = dict((node.key(), node) for node in nodes)
            digraph = "digraph{%s}" % ';'.join(node.digraph(nodes_dict) for node in nodes)
            chart_url = "http://chart.googleapis.com/chart?cht=gv&chl=%s" % urllib.quote(digraph)

            context = {
                'user': user,
                'nodes': nodes,
                'digraph': digraph,
                'chart_url': chart_url,
            }

            page = template.render('templates/index.html', context)
            self.response.out.write(page)
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        title = self.request.get('title')
        assoc_from, assoc_to = self.request.get('assoc_from'), self.request.get('assoc_to')

        if title:
            node = Node()
            node.title = title
            node.put()
        elif assoc_from and assoc_to and assoc_from.isdigit() and assoc_to.isdigit():
            node_from, node_to = Node.get_by_id(long(assoc_from)), Node.get_by_id(long(assoc_to))
            if node_from and node_to:
                node_from.associations.append(node_to.key())
                node_from.put()

        self.redirect('/')


def main():
    application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
