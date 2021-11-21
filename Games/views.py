from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import GameForms, CommentForm
from .models import Game, Comment, Vote



def game_list(request):
    all_games = Game.objects.all
    context = {"all_games": all_games}
    return render(request, "game-list.html", context)


def game_detail(request, **kwargs):
    print(kwargs)
    game_id = kwargs["pk"]
    game = Game.objects.get(id=game_id)
    user = request.user
    # has the user commented on that game already ?
    # Comments where game=specific game and user is the one requesting
    commented_already = Comment.objects.filter(game=game, user=user).exists()


    # Add comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.game = game
        # if request.user:
        # raise PermissionDenied('You have already commented on this post') DIRECT THROW - NEED IT AFTER ONE COMMENT
        if not commented_already:
            if form.is_valid():
                form.save()
                #return render(request, 'game-detail.html', {'commented_already': commented_already})
        else:
            print(form.errors)
            # RELOAD THE HTML WITH THE VALUE FOR COMMENTED ALREADY
            # return redirect('')

            # return HttpResponseRedirect(reverse('event'))
            # return render(request, 'game-detail.html', {'commented_already': commented_already})

            # return HttpResponseRedirect('/games/show/' + game_id)

            # raise PermissionDenied('You have already commented on this post')

    comments = Comment.objects.filter(game=game)
    context = {'this_game': game,
               'commented_already': commented_already,
               'comments_for_that_one_game': comments,
               'upvotes': game.get_upvotes_count(),
               'downvotes': game.get_downvotes_count(),
               'comment_form': CommentForm}
    return render(request, 'game-detail.html', context)


def vote(request, pk: str, up_or_down: str):
    game = Game.objects.get(id=int(pk))
    user = request.user
    game.vote(user, up_or_down)
    return redirect('game-detail', pk=pk)
    context = {
        "this_game": this_game,
               }
    return render(request, "game-detail.html", context)


def game_create(request):
    if request.method == "POST":
        print("I am in POST")
        create_form = GameForms(request.POST, request.FILES)
        create_form.instance.user = request.user
        if create_form.is_valid():
            create_form.save()
            print("I saved a new game")
        else:
            pass
        return redirect("game-list")
    else:
        create_form = GameForms()
        context = {"form": create_form}
        return render(request, "game-create.html", context)


def game_delete(request, **kwargs):
    game_id = kwargs["pk"]
    this_game = Game.objects.get(id=game_id)

    if request.method == "POST":
        print("I am in DELETE")
        print(request.method)

        this_game.delete()
        return redirect("game-list")
    context = {"this_game": this_game}
    return render(request, "game-delete.html", context)
