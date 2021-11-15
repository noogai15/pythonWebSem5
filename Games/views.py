from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import GameForms
from .models import Game


def game_list(request):
    all_games = Game.objects.all
    context = {"all_games": all_games}
    return render(request, "game_list.html", context)


def game_detail(request, **kwargs):
    print(kwargs)
    game_id = kwargs["pk"]
    this_game = Game.objects.get(id=game_id)
    context = {"this_game": this_game}
    return render(request, "game_details.html", context)


def game_create(request):
    if request.method == "POST":
        print("I am in POST")
        create_form = GameForms(request.POST)
        create_form.instance.user = request.user
        if create_form.is_valid():
            create_form.save()
            print("I saved a new game")
        else:
            pass
        return redirect("game_list")
    else:
        create_form = GameForms()
        context = {"form": create_form}
        return render(request, "game_create.html", context)


def game_delete(request, **kwargs):
    game_id = kwargs["pk"]
    this_game = Game.objects.get(id=game_id)

    if request.method == "POST":
        print("I am in DELETE")
        print(request.method)

        this_game.delete()
        return redirect("game_list")
    context = {"this_game": this_game}
    return render(request, "deleteConfirm.html", context)
