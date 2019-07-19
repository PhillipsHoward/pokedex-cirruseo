
from google.appengine.ext import ndb

class Type(ndb.Model):
    name = ndb.StringProperty()

class Pokemon(ndb.Model):
    name = ndb.StringProperty()
    img_url = ndb.StringProperty()
    type = ndb.StructuredProperty(Type)

#Associate an entity Trainer to a trainer_id, wich is actually a user_id.
#As every pokemon in database is child of a Trainer entity, every pokemon is thus associated to a user.
def trainer_key(trainer_id):
    return ndb.Key('Trainer', trainer_id)
