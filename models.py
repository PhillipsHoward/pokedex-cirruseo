
from google.appengine.ext import ndb

class Type(ndb.Model):
    name = ndb.StringProperty()
    color = ndb.StringProperty()

class Pokemon(ndb.Model):
    name = ndb.StringProperty()
    img_url = ndb.StringProperty()
    type = ndb.StructuredProperty(Type)

#Associate an entity Trainer to a trainer_id, wich is actually a user_id.
#As every pokemon in database is child of a Trainer entity, every pokemon is thus associated to a user.
def trainer_key(trainer_id):
    return ndb.Key('Trainer', trainer_id)

#Some basics types, in case database would be empty for some reason
def init_types():
    types = []
    fire = Type(name="Fire", color="#e25822")
    fire.put()
    types.append(fire)
    water = Type(name="Water", color="#257188")
    water.put()
    types.append(water)
    ground = Type(name="Ground", color="#BC8F8F")
    ground.put()
    types.append(ground)
    return types
