import io

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from .forms import CommentForm, GameForms, SearchForm, CommentEditForm
from .models import Comment, Game, Vote


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
    star = 0
    all_stars = [1, 2, 3, 4, 5]

    # Add comment
    if request.method == "POST":
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.game = game
        # if request.user:
        # raise PermissionDenied('You have already commented on this post') DIRECT THROW - NEED IT AFTER ONE COMMENT
        if not commented_already:
            if form.is_valid():
                form.save()
                # return render(request, 'game-detail.html', {'commented_already': commented_already})
        else:
            print(form.errors)
            # RELOAD THE HTML WITH THE VALUE FOR COMMENTED ALREADY
            # return redirect('')

            # return HttpResponseRedirect(reverse('event'))
            # return render(request, 'game-detail.html', {'commented_already': commented_already})

            # return HttpResponseRedirect('/games/show/' + game_id)

            # raise PermissionDenied('You have already commented on this post')

    comments = Comment.objects.filter(game=game)
    context = {
        "this_game": game,
        "commented_already": commented_already,
        "all_comments": comments,
        "comment_form": CommentForm,
        "star": star,
        "all_stars": all_stars,
    }
    return render(request, "game-detail.html", context)


# def vote(request, pk: str, fk: str, up_or_down: str):
#     game = Game.objects.get(id=int(game_id))
#     comment = Comment.objects.get(id=int(fk))
#     user = request.user
#     all_comments = Comment.objects.filter(game=game)
#     print(comment)
#     commented_already = Comment.objects.filter(game=game, user=user).exists()
#
#     game.vote(user, up_or_down)
#     voted_already = Vote.objects.filter(comment=comment, user=user).exists()
#
#     if voted_already:
#         print("VOTE CHECK")
#
#     context = {
#         "this_game": game,
#         "voted_already": voted_already,
#         "all_comments": all_comments,
#         'upvotes': game.get_upvotes_count(),
#         'downvotes': game.get_downvotes_count(),
#         "commented_already": commented_already
#
#     }
#     return render(request, "game-detail.html", context)


def vote(request, pk: str, fk: str, up_or_down: str):
    U_or_D = "U"
    print(up_or_down)
    if up_or_down == "down":
        U_or_D = "D"

    game = Game.objects.get(id=int(pk))
    comment = Comment.objects.get(id=int(fk))
    user = request.user
    all_comments = Comment.objects.filter(game=game)
    commented_already = Comment.objects.filter(game=game, user=user).exists()

    voted_already = Vote.objects.filter(
        up_or_down=U_or_D, comment=comment, user=user
    ).exists()

    if voted_already:
        print("ALREADY VOTED ON THIS COMMENT")
        comment.reverse_vote(user, game, U_or_D)
    else:
        print("HAD NOT VOTED ON THIS COMMENT YET")
        comment.vote(user, game, U_or_D)

    context = {
        "this_game": game,
        "voted_already": voted_already,
        "all_comments": all_comments,
        "upvotes": comment.get_upvotes_count(),
        "downvotes": comment.get_downvotes_count(),
        "commented_already": commented_already,
    }
    return redirect("game-detail", game.id)


def game_detail_pdf(request, pk: str):
    # CREATE BYTESTREAM BUFFER
    buf = io.BytesIO()
    # CREATE CANVAS
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # CREATE TEXTOBJ
    txtobj = c.beginText()
    txtobj.setTextOrigin(inch, inch)
    txtobj.setFont("Helvetica", 14)
    # ADD LINES OF TEXT
    game = Game.objects.get(id=int(pk))
    lines = [
        "Game: " + game.name,
        "Description " + game.desc,
        "Creator: " + game.creator,
        "Genre: " + game.genre,
        "Age Rating: " + str(game.age_rating),
        "Created At: " + str(game.created_at),
        "Price: " + game.price,
    ]
    # "Image " + game.image + "\n"]
    # txt = ["Game: " + game.name + "Description: " + game.desc + "Creator: " + game.creator];
    # game_detail_pdf(txt)
    # LOOP
    for line in lines:
        txtobj.textLine(line)

    # FINISH UP
    c.drawText(txtobj)
    c.showPage()
    c.save()
    buf.seek(0)

    # RETURN SMTH
    return FileResponse(buf, as_attachment=True, filename="venue.pdf")


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


def game_search(request):
    if request.method == 'POST':
        search_string_creator = request.POST['creator']
        games_found = Game.objects.filter(creator__contains=search_string_creator)

        search_string_name = request.POST['name']
        if search_string_name:
            games_found = games_found.filter(name__contains=search_string_name)

        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'games_found': games_found,
                   'show_results': True}
        return render(request, 'game-search.html', context)

    else:
        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'show_results': False}
        return render(request, 'game-search.html', context)


def edit_comment(request, pk, comment_id):
    comment_edit_form = CommentEditForm(request.POST if request.POST else None, instance= Comment.objects.get( ))


class UpdateCommentView(UpdateView):
    model = Comment
    template_name = 'comment-edit.html'
    form_class = CommentEditForm
    success_url = reverse_lazy("game-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

