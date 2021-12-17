import io

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.http import FileResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, UpdateView
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from Shoppingcart.models import ShoppingCart

from .forms import CommentEditForm, CommentForm, GameForms, SearchForm
from .models import Comment, Game, Report, Vote


# VON JEDEM ABRUFBAR
def game_list(request):
    all_games = Game.objects.all
    context = {"all_games": all_games}
    return render(request, "game-list.html", context)


# VON JEDEM ABRUFBAR
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


# JEDER DARF JEDEN KOMMENTAR VOTEN
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


# JEDER DARF SICH PDFs zum Spiel herunterladen
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
    return FileResponse(buf, as_attachment=True, filename=game.name + ".pdf")


# NUR CS/SU DÜRFEN SPIELE ERSTELLEN
@permission_required(
    "games.add_game"
)  # WORKS : CUSTOMER NOT ALLOWED / BUT SUPERUSER & CS are
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


# NUR CS/SU DÜRFEN SPIELE LÖSCHEN
@permission_required(
    "games.delete_game"
)  # WORKS : CUSTOMER NOT ALLOWED / BUT SUPERUSER & CS are
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


# NUR CS/SU DÜRFEN SPIELE UPDATEN zB. bei Preisänderung
# EDIT GAME (maybe not needed)

# DARF JEDER
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


# JEDER DARF SEINEN EIGENEN KOMMENTAR EDITIEREN &&& CS/SU DÜRFEN ALLE ÄNDERN
class UpdateCommentView(UpdateView):  # PermissionRequiredMixin,
    # SO KANN DER USER SEINE EIGENEN KOMMENTARE NICHT EDITIEREN
    # raise_exception = True
    # permission_required = 'Games.change_comments'
    # permission_denied_message = ""
    # login_url = "/games/"
    # redirect_field_name = next

    model = Comment
    template_name = "comment-edit.html"
    form_class = CommentEditForm
    success_url = reverse_lazy("game-list")

    def form_valid(self, form):
        # WIE CHECKEN WIR HIER OB DAS SEIN EIGENER KOMMENTAR IST
        # DEN BUTTON ALLEIN WEGRENDERN REICHT NICHT, DA DER LINK NOCH ABRUFBAR IST
        form.instance.myuser = self.request.user
        return super().form_valid(form)


# JEDER DARF SEINEN EIGENEN KOMMENTAR LÖSCHEN &&& CS/SU DARF ALLE LÖSCHEN
class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "comment-delete.html"
    form_class = CommentEditForm
    success_url = reverse_lazy("game-list")

    def form_valid(self, form):
        form.instance.myuser = self.request.user
        return super().form_valid(form)


# JEDER DARF JEDEN REPORTEN
def comment_report(request, pk: int, game_id: str):
    user = request.user
    game = Game.objects.get(id=game_id)
    comment = Comment.objects.get(id=int(pk))
    comment.report(user)
    # IF COMMENT HAS BEEN REPORTED ALREADY :
    reported_already = Report.objects.filter(reporter=user, comment=comment).exists()
    # commented_already = Comment.objects.filter(game=game, user=user).exists()

    return redirect("game-detail", game.id)


def game_cart(request):  # , pk: int
    context = {}
    return render(request, "game-cart.html", context)


def cart_add_game(request, game_id: int):
    game = Game.objects.get(id=game_id)
    myuser = request.user

    if game:
        ShoppingCart.add_item(myuser, game)
    return redirect("game-detail", game.id)
