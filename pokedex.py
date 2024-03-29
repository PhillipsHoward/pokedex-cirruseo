
import jinja2
import webapp2
import os
import urllib

from google.appengine.api import users
from google.appengine.api import urlfetch

from models import Pokemon, Type, init_types
from queries import fetch_types, fetch_pokemons_list, trainer_key

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
MAX_LENGHT_NAME = 75

class MainPage(webapp2.RequestHandler):

    def get(self):

        #Authenticate user and fetch informations in database
        user = users.get_current_user()
        url_logout = users.create_logout_url('/')
        types = fetch_types()
        pokemons = fetch_pokemons_list(user.user_id())

        #Generate the page
        template_values = {
            'user' : user,
            'types' : types,
            'pokemons': pokemons,
            'url_logout' : url_logout,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class CapturePokemon(webapp2.RequestHandler):

    #Call a G Cloud Function wich returns an url of a pokemon image based on the pokemon name.
    def get_pokemon_image(self, pokemon_name):
        url_pic_gfunction = "https://us-central1-pokedex-cirrusetest.cloudfunctions.net/get_img_pokemon?pokemon="+urllib.quote(pokemon_name.encode('utf8'))
        try: #If fails, return metamorph image by default : ("...132.png")
            result = urlfetch.fetch(url_pic_gfunction)
            if result.status_code == 200:
                return result.content
            else:
                self.response.status_code = result.status_code
                return "/assets/mysterepokemon.png"
        except urlfetch.Error:
            return "/assets/mysterepokemon.png"

    #Create a pokemon object ready to be pushed into the database
    def make_pokemon(self, name, type_name):
        trainer_id = users.get_current_user().user_id()
        pokemon = Pokemon(parent=trainer_key(trainer_id)) #Define a Trainer as the parent of the new pokemon. This trainer's key is the current user id. Thus every user has his own pokemon list
        pokemon.img_url = self.get_pokemon_image(name)
        pokemon.name = name
        pokemon.type = Type.query(Type.name == type_name).get()
        return pokemon

    #Push a new pokemon into the database
    def post(self):

        #Pokemon name should not be empty. If it's the case, replace it by this nice smiley.
        if self.request.get('name').isspace() or self.request.get('name') == "" :
            pokemon_name = "0_0"
        #Pokemon name should not be longer than a certain number
        elif len(self.request.get('name')) > MAX_LENGHT_NAME:
            pokemon_name = self.request.get('name')[:MAX_LENGHT_NAME]
        else :
            pokemon_name = self.request.get('name')

        type_name = self.request.get('type_name')
        pokemon = self.make_pokemon(pokemon_name, type_name)

        trainer_id = users.get_current_user().user_id()
        if pokemon_name not in [poke.name for poke in fetch_pokemons_list(trainer_id)]: # Check if new pokemon does not already exist in user pokedex (checking it by name)
            pokemon.put()
        self.redirect('/')

#Entry point ot the app. The WGSI Application receives requests and dispatches the appropriate handlers.
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/capture', CapturePokemon),
], debug=False)
