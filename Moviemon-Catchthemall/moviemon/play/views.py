from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from .data_mgmt import Data_mgmt
from random import randint
from django.http import Http404
from moviemon.settings import MAP, SESSION

def title_screen(request):
    context = {"controls": {"a": {"action": "worldmap", "value": "default_settings"}, "b": {"action": "options/load_game", "value": "load"} } }
    dat = Data_mgmt()
    dat.load_default_settings()
    dat.dump_session()
    return render(request, "play/title_screen.html", context)

def worldmap(request):
    data = Data_mgmt().load(SESSION)
    chance = randint(0,3)
    data.set_Status(0)
    mapping = { "W": range(settings.MAP["W"]), "H": range(settings.MAP["H"]) }
    if request.method == 'POST' and request._get_post()['clicked']:
        val = request._get_post()['val']
        if chance == 1:
            data.nbr_balls = data.nbr_balls + 1
        if val == "left" and data.position['x'] > 0:
            data.position['x'] = data.position['x'] - 1
        if val == "up" and data.position['y'] > 0:
            data.position['y'] = data.position['y'] - 1
        if val == "right" and data.position['x'] <= 9:
            data.position['x'] = data.position['x'] + 1
        if val == "down" and data.position['y'] <= 9:
            data.position['y'] = data.position['y'] + 1
        if val == "default_settings":
            Data_mgmt().load_default_settings()
    def attack_link():
        if chance == 2:
            v = Data_mgmt().get_random_movie()#Get a randome attack
            return "battle/" + str(v['imdbID'])
            # return "battle/tt0421051"# MORE SIMPLE FOR TEST
        else:
            return ""

    position = data.position
    if position["x"] != 0:
        left = {"action": "worldmap", "value": "left"}
    else:
        left = {"action": "", "value": ""}
    if position["y"] != 0:
        up = {"action": "worldmap", "value": "up"}
    else:
        up = {"action": "", "value": ""}
    if position["x"] != int(settings.MAP["H"]) - 1 and data.position['x'] < 10:
        right = {"action": "worldmap", "value": "right"}
    else:
        right = {"action": "", "value": ""}
    if position["y"] != int(settings.MAP["H"]) - 1 and data.position['y'] < 10:
        down = {"action": "worldmap", "value": "down"}
    else:
        down = {"action": "", "value": ""}
    controls = {
            "left": left,
            "up": up,
            "right": right,
            "down": down,
            "a": {"action": attack_link(), "value": attack_link()},
            "start": {"action": "/options", "value": "options"},
            "select": {"action": "/moviedex", "value": "moviedex"},
            }
    context = { "map": mapping, "controls": controls, "position": position, 'balls' : data.nbr_balls }
    data.dump_session()
    return render(request, "play/worldmap.html", context)

def moviedex(request):
    data = Data_mgmt().load(SESSION)
    # datamg.load_default_settings() 
    if request.method == 'POST' and request._get_post()['clicked']:
        val = request._get_post()['val']
    movies = data.moviedex
    j = data.movie_index
    if val == "detail":
        return HttpResponseRedirect("/moviedex/" + movies[j]["imdbID"])
    if val == "left":
        if j < 1:
            j = len(movies) - 1
        else:
            j -= 1
    if val == "right":
        j += 1
        if j >= len(movies):
            j = 0
    if len(movies) == 0:
        j = -1
    data.movie_index = j
    controls = {
            "left": {"action": "moviedex", "value": "left"},
            "right": {"action": "moviedex", "value": "right"},
            "a": {"action": "moviedex", "value": "detail"},
            "select": {"action": "worldmap", "value": "back"},
            }
    context = {"j":j, "controls":controls}
    if j != -1:
        context["movies"] = movies[j]
    else:
        controls['a']['value'] = ''
        controls['right']['value'] = ''
        controls['left']['value'] = ''
    data.dump_session()
    return render(request, "play/moviedex.html", context)

def battle(request):
    context = {}
    return render(request, "play/battle.html", context)

def battle_moviemon(request, moviemon_id):
    dump = Data_mgmt().load(SESSION)
    status = ""
    mov = dict()
    if request.method == 'POST' and request._get_post()['clicked']:
        val = request._get_post()['val']
        if val == "throw":
            if dump.get_Status() == 1:
                dump.nbr_balls = dump.nbr_balls - 1
            dump.dump_session()
            # dat.load(dump["position"], dump.nbr_balls., dump.Moviedex)
        balls = dump.nbr_balls
        sgt = dump.get_strength()
        for item in dump.movielist:
            if item['imdbID'] == moviemon_id:
                mov = item

    if len(mov) == 0:
        raise Http404("Error with movie ID")
    taux  =  50 + float(sgt) * 5 - float(mov['imdbRating'][0:1]) * 10
    if taux < 1:
        taux = 1
    elif taux > 90:
        taux = 90

    if int(balls) <= 0:
        status = "Moviemon : You have no balls biatch !!"
    elif dump.get_Status() == 1:#Je suis deja venu
        if randint(1, 100) < taux:
            status = "You catched it !"
            dump.movie_index = 0
            dump.set_Status(2)
            dump.strength += 1
            if mov not in dump.moviedex:
                dump.moviedex.append(mov)# dump.get_movie(dump["Moviedex"]))
            dump.dump_session()
        else:
            status = "You missing the moviemon, Try hard and drink more coffee !"
    elif dump.get_Status() == 0:
        status = "You find a moviemon, Try to catch him !"
    else:
        status = "You have captured this moviemon, gratz !"

    if int(balls) > 0 and dump.get_Status() != 2:
        launch = {"action": "/battle/"+moviemon_id, "value":"throw"}
    else:
        launch = {"action": "", "value": ""}

    controls = {
            "left": {"action": "", "value": ""},
            "up": {"action": "", "value": ""},
            "right": {"action": "", "value": ""},
            "down": {"action": "", "value": ""},
            "a": launch,
            "b": {"action": "/worldmap", "value": "worldmap"},
            "start": {"action": "", "value": ""},
            "select": {"action": "", "value": ""},
            }
    if dump.get_Status() == 0:
        dump.set_Status(1)
    dump.dump_session()
    context = {"moviemon": mov, "nbr_balls" : balls, "strength" : sgt, "taux" : taux, "controls": controls, "status": status}

    #ELSE GET ->
    # content ->
    return render(request, "play/battle_moviemon.html", context)


def moviedex_moviemon(request, moviemon_id):
    data = Data_mgmt().load(SESSION)
    movies = data.movielist
    for elem in movies:
        if elem['imdbID'] == moviemon_id:
            movie = elem
    controls = {
            "b": {"action": "/moviedex", "value": "back"},
            }
    context = {"movie": movie, "controls":controls}
    return render(request, "play/moviedex_moviemon.html", context)

def options(request):
    controls = {
            "start": {"action": "/worldmap", "value": "start"},
            "a": {"action": "/options/save_game", "value": "a"},
            "b": {"action": "/", "value": "b"},
            }
    context = {"controls":controls}
    return render(request, "play/options.html", context)

def options_save_game(request):
    data = Data_mgmt().load(SESSION)
    saves = data.get_all_save()
    if request.method == 'POST':
        val = request._get_post()['val']
        if val == "a":
            if data.Boli == False:
                data.index = 1
                data.Boli = True
                controls = {
                        "up": {"action": "", "value": "up"},
                        "down": {"action": "", "value": "down"},
                        "a": {"action": "/options/save_game", "value": "a"},
                        "b": {"action": "/options", "value": "b"},
                        }
                context = {"controls":controls, 'saves' : saves}
                data.dump_session()
                return HttpResponseRedirect('/options/save_game')
            old = None
            if len(saves[data.index - 1]) == 2:
                old = saves[data.index - 1][1]
            data.save_game('abc'[data.index - 1], old)
            saves = data.get_all_save()
        elif val == 'b':
            data.Boli == False
            data.dump_session()
            return HttpResponseRedirect('/options')
        if val == 'down':
            data.index += 1
            if data.index > 3:
                data.index = 3
        elif val == 'up':
            data.index -= 1
            if data.index < 1:
                data.index = 1
    else:
        data.index = 1

    controls = {
            "up": {"action": "", "value": "up"},
            "down": {"action": "", "value": "down"},
            "a": {"action": "/options/save_game", "value": "a"},
            "b": {"action": "/options", "value": "b"},
            }
    context = {"controls":controls, 'saves' : saves, 'data' : data}
    data.dump_session()
    return render(request, "play/options_save_game.html", context)

def options_load_game(request):
    data =  Data_mgmt().load(SESSION)
    saves = data.get_all_save()
    val = request._get_post()['val']
    if val == 'down':
        data.index += 1
        if data.index > 3:
            data.index = 3
    if val == 'up':
        data.index -= 1
        if data.index < 1:
            data.index = 1
    if val == "a":
        game = None
        
        if len(saves[data.index - 1]) == 2:
            game = saves[data.index - 1][1]
            data = data.load_save(game)
            controls = {
                    "up": {"action": "", "value": "up"},
                    "down": {"action": "", "value": "down"},
                    "a": {"action": "/worldmap", "value": "a"},
                    "b": {"action": "/", "value": "b"},
                    }
            context = {"controls": controls, 'saves' : saves}
            data.dump_session()            
            return HttpResponseRedirect("/worldmap")
            
    if val == "b":
        pass
    controls = {
            "up": {"action": "", "value": "up"},
            "down": {"action": "", "value": "down"},
            "a": {"action": "/options/load_game", "value": "a"},
            "b": {"action": "/", "value": "b"},
            }
    context = {"controls": controls, 'saves' : saves, 'data' : data}
    data.dump_session()
    
    return render(request, "play/options_load_game.html", context)
