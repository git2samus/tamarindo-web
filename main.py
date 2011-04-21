#!/usr/bin/env python
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from views import MainHandler


def main():
    application = WSGIApplication([('/', MainHandler)], debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

