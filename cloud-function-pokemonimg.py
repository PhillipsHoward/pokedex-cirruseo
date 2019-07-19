api_url_base = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/"

#From a pokemon name, generate an url wich returns a pokemon image
def build_url(pokemon) :
    prefix_id = ""

    #Calculate the ASCII value sum of pokemon name characters, then apply a modulo
    #to get a number between 0 and 150. (the number of pokemons first generation).
    #This is arbitrary : but it works.
    ascii_sum = 0
    for char in pokemon:
        ascii_sum += ord(char)
    img_id = ascii_sum %150

    #If img id = 0, reset it to 132 (Metamorph id)
    if img_id == 0 :
        img_id = 132

    #The Pokemon API only accepts this id format : 00x or 0xx. So you need to add 0 or 00 if necessary.
    if img_id < 10 :
         prefix_id = "00"
    elif img_id < 100 :
        prefix_id = "0"

    return api_url_base+prefix_id+str(img_id)+".png"

def get_pokemon_image(request):

    request_json = request.get_json()

    if request.args and 'pokemon' in request.args:
        pokemon = request.args.get('pokemon')
        return build_url(pokemon)

    elif request_json and 'pokemon' in request_json:
        pokemon = request_json['pokemon']
        return build_url(pokemon)

    else:
        return api_url_base + "132.png"
