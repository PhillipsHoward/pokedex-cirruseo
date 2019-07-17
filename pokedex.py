
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
    #type_key = ndb.KeyProperty(kind='Type', repeated=True)
    type = ndb.StringProperty()

# HANDLERS

class MainPage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        url_logout = users.create_logout_url('/')

        trainer_id = user.user_id()
        pokemons_query = Pokemon.query(
            ancestor=trainer_key(trainer_id))
        pokemons = pokemons_query.fetch(10)

        template_values = {
            'user' : user,
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
        print type_name
        pokemon.type = type_name
        pokemon.put()

        self.redirect('/')

    def get_type(self, type_name):
        type = Type.query(Type.name == type_name )
        if type.key is None :
            type = Type(name=type_name)
            return type.put()
        else :
            return type


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/capture', CapturePokemon),
], debug=True)
