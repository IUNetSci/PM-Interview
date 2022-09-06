'''
Instructions
    1) Create a github repository (or fork the repo that this is found in)
    2) Create user documentation for the following REST API
        a) Be as detailed and consice as possible
        b) Include an introduction
        c) Can be in whatever format you want
        d) Documentation will be used by future developers to create apps using this API
        e) Try to keep the documentation under 500 words.
        f) Shouldn't take more than a couple of hours
    3) Use github to host the documentation
    4) Make sure that documentation is public and available to us

'''



import server_thing
import database_magic
import ai_duck_generator

app = server_thing()

app.add_route('/api/duck/create', 'POST')
def create_duck(request):
    duck_settings = request.getJSON()
    result = database_magic.query("INSERT $color, $size INTO `ducks`",
        duck_settings["color"],
        duck_settings["size"]
    )
    if result:
        return 201
    else:
        return 500

app.add_route('/api/duck/delete/<duck_id>', 'POST')
def delete_duck(request, duck_id):
    result = database_magic.query("DELETE FROM `ducks` WHERE `id` = $id", duck_id)
    if result == 'success':
        return 204
    elif result == 'not found':
        return 404, "DUCK NOT FOUND"
    else:
        return 500

app.add_route('/api/duck/update/<duck_id>', 'POST')
def update_duck(request, duck_id):
    new_settings = request.getJSON()
    result = database_magic.query("UPDATE `ducks` SET $color, $size WHERE `id` = $id", new_settings["color"], new_settings["size"], duck_id)
    if result == 'success':
        return 204
    elif result == 'not found':
        return 404, "DUCK NOT FOUND"
    else:
        return 500

app.add_route('/api/duck/<duck_id>/quack', "GET")
def quack(request, duck_id):
    duck = database_magic.query("GET FROM `ducks` WHERE `id` = $id", duck_id)
    if duck:
        return 200, "THE $size, $color DUCK GOES QUACK!!".format(duck["size"], duck["color"])
    else:
        return 404, "DUCK NOT FOUND"

app.add_route('/api/duck/picture/<duck_id>', "GET")
def quack(request, duck_id):
    duck = database_magic.query("GET FROM `ducks` WHERE `id` = $id", duck_id)
    if not duck:
        return 404, "DUCK NOT FOUND"
    picture = ai_duck_generator(duck["color"], duck["size"])
    if picture:
        return 200, picture
    else:
        return 500
    