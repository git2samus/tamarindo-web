import urllib

from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template

from models import Node


class MainHandler(RequestHandler):
    def get(self):
        user = users.get_current_user()

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
            'logout_url': users.create_logout_url('/')
        }

        page = template.render('templates/index.html', context)
        self.response.out.write(page)

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

