from google.appengine.ext import ndb

class Planner(ndb.Model):
    date = ndb.StringProperty()
    task = ndb.StringProperty()
    completed = ndb.StringProperty(default="NE")