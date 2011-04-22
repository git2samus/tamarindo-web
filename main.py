#!/usr/bin/env python
from google.appengine.dist import use_library
use_library('django', '1.2')

import os

from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from views import *


def main():
    urlconf = [
        ('/', DashboardHandler),
    ]

    debug = os.environ['SERVER_SOFTWARE'].startswith('Development')
    application = WSGIApplication(urlconf, debug=debug)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

