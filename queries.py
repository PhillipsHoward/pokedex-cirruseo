from google.appengine.ext import ndb
from models import Pokemon, Type

#Fetch types list. If there is no types in database, populate it.
def fetch_types():
    type_query = Type.query()
    types = type_query.fetch()

    if not types :
        return init_types()
    else :
        return types

#Fetch pokemons in user pokedex
def fetch_pokemons_list(trainer_id, number_to_fetch=None):
    pokemons_query = Pokemon.query(
        ancestor=trainer_key(trainer_id))
    pokemons = pokemons_query.order(Pokemon.name).fetch(number_to_fetch)
    return pokemons

#Associate an entity Trainer to a trainer_id, wich is actually a user_id.
#As every pokemon in database is child of a Trainer entity, every pokemon is thus associated to a user.
def trainer_key(trainer_id):
    return ndb.Key('Trainer', trainer_id)
