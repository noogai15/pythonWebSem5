import io

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.http import FileResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, UpdateView
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.contrib.auth import get_user_model

from .forms import CommentEditForm, CommentForm, GameForms, SearchForm
from .models import Comment, Game, Report, Vote


def game_list(request):
    all_games = Game.objects.all
    context = {"all_games": all_games}
    return render(request, "game-list.html", context)


def game_detail(request, **kwargs):
    print(kwargs)
    game_id = kwargs["pk"]
    game = Game.objects.get(id=game_id)
    myuser = request.user
    # has the user commented on that game already ?
    # Comments where game=specific game and user is the one requesting
    commented_already = Comment.objects.filter(game=game, myuser=myuser).exists()
    star = 0
    all_stars = [1, 2, 3, 4, 5]

    # Add comment

    if request.method == "POST":
        form = CommentForm(request.POST)
        form.instance.myuser = request.user
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
    comments_length = Comment.objects.filter(game=game).count()
    if comments.count() == comments_length and comments.count() != 0:
        i = 0
        c = 0
        for comment in comments:
            i += comment.star_rating
            c += 1

        result = int(round(i / c))
        average_stars = result
        game.average_stars = average_stars
        game.save()
        print(average_stars)
    else:
        average_stars = 0
        game.average_stars = average_stars
        game.save()

    context = {
        "this_game": game,
        "commented_already": commented_already,
        "all_comments": comments,
        "comment_form": CommentForm,
        "star": star,
        "all_stars": all_stars,
        "average_stars": average_stars,
    }
    return render(request, "game-detail.html", context)


def get_average_star_rating(self):

    all_comments = Comment.objects.filter(game=self)
    result = 0
    current_length_of_comments = Comment.objects.filter(game=self).count()
    # CHECK IF A COMMENT HAS BEEN ADDED THEN DO THE SAME AGAIN TO UPDATE ATTRIBUTE AVERAGE_STARS

    # CHECK IF THEY ARE THE SAME LENGTH

    # else:
    # result = 0
    # self.average_stars = 0

    return result


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
    myuser = request.user
    all_comments = Comment.objects.filter(game=game)
    commented_already = Comment.objects.filter(game=game, myuser=myuser).exists()

    voted_already = Vote.objects.filter(
        up_or_down=U_or_D, comment=comment, myuser=myuser
    ).exists()

    if voted_already:
        print("ALREADY VOTED ON THIS COMMENT")
        comment.reverse_vote(myuser, game, U_or_D)
    else:
        print("HAD NOT VOTED ON THIS COMMENT YET")
        comment.vote(myuser, game, U_or_D)

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
        "Rating: " + str(game.average_stars),
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
        create_form.instance.myuser = request.user
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
    if request.method == "POST":
        # SEARCH WITH : DESCRIPTION
        search_string_name = request.POST["name"]
        games_found = Game.objects.filter(name__contains=search_string_name)

        # SEARCH WITH : NAME
        search_string_desc = request.POST["desc"]
        if search_string_desc:
            games_found = games_found.filter(desc__contains=search_string_desc)

        # SEARCH WITH : STAR - RATING
        search_average_stars = request.POST["average_stars"]
        if search_average_stars:
            games_found = games_found.filter(average_stars__exact=search_average_stars)

        form_in_function_based_view = SearchForm()
        context = {
            "form": form_in_function_based_view,
            "games_found": games_found,
            "show_results": True,
        }
        return render(request, "game-search.html", context)

    else:
        form_in_function_based_view = SearchForm()
        context = {"form": form_in_function_based_view, "show_results": False}
        return render(request, "game-search.html", context)


def edit_comment(request, pk, comment_id):
    comment_edit_form = CommentEditForm(
        request.POST if request.POST else None, instance=Comment.objects.get()
    )


class UpdateCommentView(UpdateView):
    model = Comment
    template_name = "comment-edit.html"
    form_class = CommentEditForm
    success_url = reverse_lazy("game-list")

    def form_valid(self, form):
        form.instance.myuser = self.request.user
        return super().form_valid(form)


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "comment-delete.html"
    form_class = CommentEditForm
    success_url = reverse_lazy("game-list")

    def form_valid(self, form):
        form.instance.myuser = self.request.user
        return super().form_valid(form)


def comment_report(request, pk: int, game_id: str):
    user = request.user
    game = Game.objects.get(id=game_id)
    comment = Comment.objects.get(id=int(pk))
    comment.report(user)
    # IF COMMENT HAS BEEN REPORTED ALREADY :
    reported_already = Report.objects.filter(reporter=user, comment=comment).exists()
    # commented_already = Comment.objects.filter(game=game, user=user).exists()

    return redirect("game-detail", game.id)
