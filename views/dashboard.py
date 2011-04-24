from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template

from models import Project
from utils import context_dict


class DashboardHandler(RequestHandler):
    def get(self):
        user = users.get_current_user()

        projects = Project.all()
        projects.filter("owner =", user.user_id())
        projects.order("title")
        projects = tuple(projects) # prevent re-execution when iterating

        context = context_dict(locals(), 'user', 'projects')
        context['logout_url'] = users.create_logout_url('/')

        page = template.render('templates/dashboard.html', context)
        self.response.out.write(page)

    def post(self):
        user = users.get_current_user()

        title = self.request.get('title')
        if title:
            new_project = Project(
                owner=user.user_id(),
                title=title,
            )
            new_project.put()

            self.redirect(new_project.permalink)
            return

        self.redirect('/')

