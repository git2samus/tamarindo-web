import urllib

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import RequestHandler, template

from models import Project, Node
from utils import context_dict


def decorator(f):
    def wrapper(self, project_id):
        project = Project.get_by_id(long(project_id))
        if project:
            user = users.get_current_user()
            if project.owner == user.user_id():
                nodes = Node.all()
                nodes.ancestor(project)
                nodes.order('title')
                nodes = tuple(nodes) # prevent re-execution when iterating

                request_node, current_node = self.request.get('node'), None
                if request_node: # self.request.get always return a string
                    try:
                        current_node_id = long(request_node)
                    except ValueError:
                        pass
                    else:
                        for node in nodes:
                            if node.key().id() == current_node_id:
                                current_node = node
                                break
                    if current_node is None:
                        self.redirect(project.permalink)
                        return

                f(self, user, project, nodes, current_node)
            else:
                self.error(403)
        else:
            self.redirect('/')

    return wrapper


class ProjectHandler(RequestHandler):
    @decorator
    def get(self, user, project, nodes, current_node=None):
        nodes_dict = dict((node.key(), node) for node in nodes)
        digraph = "digraph{%s}" % ';'.join(node.digraph(nodes_dict) for node in nodes)
        chart_url = "http://chart.googleapis.com/chart?cht=gv&chl=%s" % urllib.quote(digraph)

        context = context_dict(locals(), 'user', 'project', 'nodes', 'current_node', 'digraph', 'chart_url')
        context['logout_url'] = users.create_logout_url('/')

        page = template.render('templates/project.html', context)
        self.response.out.write(page)

    @decorator
    def post(self, user, project, nodes, current_node=None):
        title = self.request.get('title')
        if title:
            def transaction():
                q = Node.all()
                q.ancestor(project)
                q.filter('title =', title)
                node = q.get()

                if node is None:
                    node = Node(
                        parent=project,
                        title=title,
                    )
                    node.put()

                return node

            node = db.run_in_transaction(transaction)

            self.redirect(node.permalink)
            return

        if current_node:
            try:
                association_id = long(self.request.get('association'))
            except ValueError:
                pass
            else:
                association = Node.get_by_id(association_id, parent=project)
                if association:
                    current_node.associations.append(association.key())
                    current_node.put()

                    self.redirect(current_node.permalink)
                    return

        self.redirect(project.permalink)

