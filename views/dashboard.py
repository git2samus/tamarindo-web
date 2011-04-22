from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template


class DashboardHandler(RequestHandler):
    def get(self):
        user = users.get_current_user()

        context = {
            'user': user,
        }

        page = template.render('templates/dashboard.html', context)
        self.response.out.write(page)

