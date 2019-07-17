
import jinja2
import webapp2
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

#CONSTANTS

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def trainer_key(trainer_id):
    return ndb.Key('Trainer', trainer_id)

# MODELS

class Type(ndb.Model):
    name = ndb.StringProperty()

class Pokemon(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StructuredProperty(Type)

# HANDLERS

class MainPage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        url_logout = users.create_logout_url('/')

        type_query = Type.query()
        types = type_query.fetch(10)

        if not types :
            fire = Type(name="Fire")
            fire.put()
            water = Type(name="Water")
            water.put()
            earth = Type(name="Earth")
            earth.put()


        trainer_id = user.user_id()
        pokemons_query = Pokemon.query(
            ancestor=trainer_key(trainer_id))
        pokemons = pokemons_query.fetch(10)

        template_values = {
            'user' : user,
            'types' : types,
            'pokemons': pokemons,
            'url_logout' : url_logout,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class CapturePokemon(webapp2.RequestHandler):

    def post(self):

        user = users.get_current_user()
        trainer_id = user.user_id()
        pokemon = Pokemon(parent=trainer_key(trainer_id))
        pokemon.name = self.request.get('name')
        type_name = self.request.get('type')
        type_query = Type.query(Type.name == type_name)
        type = type_query.get()
        pokemon.type = type
        pokemon.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/capture', CapturePokemon),
], debug=True)
