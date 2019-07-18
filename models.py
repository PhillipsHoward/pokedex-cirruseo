
from google.appengine.ext import ndb

class Type(ndb.Model):
    name = ndb.StringProperty()

class Pokemon(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StructuredProperty(Type)

def trainer_key(trainer_id):
    return ndb.Key('Trainer', trainer_id)
