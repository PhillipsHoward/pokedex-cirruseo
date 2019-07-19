
from google.appengine.ext import ndb

class Type(ndb.Model):
    name = ndb.StringProperty()
    color = ndb.StringProperty()

class Pokemon(ndb.Model):
    name = ndb.StringProperty()
    img_url = ndb.StringProperty()
    type = ndb.StructuredProperty(Type)

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
