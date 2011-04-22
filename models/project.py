from google.appengine.ext import db


class Project(db.Model):
    # owner should be a UserProperty but at this moment it's useless
    # since it does not remain valid when the user changes his email
    # we'll use User.user_id() instead.
    owner = db.StringProperty()
    title = db.StringProperty()

