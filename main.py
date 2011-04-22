#!/usr/bin/env python
from google.appengine.dist import use_library
use_library('django', '1.2')

import os

from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from views import MainHandler


def main():
    debug = os.environ['SERVER_SOFTWARE'].startswith('Development')

    application = WSGIApplication([('/', MainHandler)], debug=debug)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

