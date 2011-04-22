from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template

from models import Project


class DashboardHandler(RequestHandler):
    def get(self):
        user = users.get_current_user()

        projects = Project.all()
        projects.filter("owner =", user.user_id())
        projects.order("title")
        projects = tuple(projects) # prevent re-execution when iterating

        context = {
            'user': user,
            'projects': projects,
        }

        page = template.render('templates/dashboard.html', context)
        self.response.out.write(page)

    def post(self):
        user = users.get_current_user()

        title = self.request.get('title')
        if title:
            Project(
                owner=user.user_id(),
                title=title,
            ).put()

        self.redirect('/')
