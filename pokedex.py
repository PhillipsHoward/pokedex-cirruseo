
import jinja2
import webapp2
import os
import urllib

from google.appengine.api import users
from google.appengine.api import urlfetch
from models import Pokemon, Type, trainer_key

#CONSTANTS

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# HANDLERS

class MainPage(webapp2.RequestHandler):

    def _init_types(self):
        type_query = Type.query()
        types = type_query.fetch(10)

        if not types :
            fire = Type(name="Fire")
            fire.put()
            water = Type(name="Water")
            water.put()
            earth = Type(name="Earth")
            earth.put()
            types = type_query.fetch(10)
        return types

    def get(self):

        user = users.get_current_user()
        url_logout = users.create_logout_url('/')

        types = self._init_types()

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

    def get_pokemon_image(self, pokemon_name):
        pokemon_name = pokemon_name.replace(" ", "")
        url_pic_gfunction = "https://us-central1-pokedex-cirrusetest.cloudfunctions.net/get_img_pokemon?pokemon="+pokemon_name
        try:
            result = urlfetch.fetch(url_pic_gfunction)
            if result.status_code == 200:
                return result.content
            else:
                self.response.status_code = result.status_code
                return "https://assets.pokemon.com/assets/cms2/img/pokedex/full/132.png"
        except urlfetch.Error:
            return "https://assets.pokemon.com/assets/cms2/img/pokedex/full/132.png"

    def make_pokemon(self, name, type_name):
        trainer_id = users.get_current_user().user_id()
        pokemon = Pokemon(parent=trainer_key(trainer_id))
        pokemon.img_url = self.get_pokemon_image(name)
        pokemon.name = name
        pokemon.type = Type.query(Type.name == type_name).get()
        return pokemon

    def post(self):
        pokemon_name = self.request.get('name')
        type_name = self.request.get('type_name')
        pokemon = self.make_pokemon(pokemon_name, type_name)
        pokemon.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/capture', CapturePokemon),
], debug=True)
