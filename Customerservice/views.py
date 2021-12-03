from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView
from Games.models import Comment, Report

from .forms import CS_CommentEditForm

# Create your views here.


class CS_CommentDeleteView(ListView):
    model = Comment
    context_object_name = "all_the_comments"
    template_name = "cs-comment-delete.html"

    def get_context_data(self, **kwargs):
        context = super(CS_CommentDeleteView, self).get_context_data(**kwargs)
        can_delete = False
        myuser = self.request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        context["can_delete"] = can_delete
        return context

    def post(self, request, *args, **kwargs):
        comment_id = request.POST["comment_id"]
        if "delete" in request.POST:
            Comment.objects.get(id=comment_id).delete()
            return redirect("cs-comment-delete")


class CS_CommentEditView(UpdateView):
    model = Comment
    form_class = CS_CommentEditForm
    template_name = "cs-comment-edit.html"
    success_url = reverse_lazy("cs-comment-delete")

    def get_context_data(self, **kwargs):
        context = super(CS_CommentEditView, self).get_context_data(**kwargs)
        can_delete = False
        myuser = self.request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        context["can_delete"] = can_delete
        return context


# @staff_member_required(login_url='/useradmin/login/')
def comment_edit_delete(request, pk: str):
    comment_id = pk
    if request.method == "POST":
        print("-------------", request.POST)
        if "edit" in request.POST:
            form = CS_CommentEditForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.get(id=comment_id)
                new_text = form.cleaned_data["text"]
                comment.text = new_text
                comment.save()
        elif "delete" in request.POST:
            Comment.objects.get(id=comment_id).delete()

        return redirect("cs-comment-delete")

    else:
        can_delete = False
        myuser = request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        comment = Comment.objects.get(id=comment_id)
        form = CS_CommentEditForm(request.POST or None, instance=comment)
        context = {
            "form": form,
            "can_delete": can_delete,
            "comment": comment,
        }
        return render(request, "cs-comment-edit-delete.html", context)


def get_all_reports(request):
    all_reports = Report.objects.all()
    context = {"reports": all_reports}

    return render(request, "all_reports.html", context)


def delete_comment(
    request,
    pk: int,
):

    try:
        comment = Comment.objects.get(id=int(pk))
    except Comment.DoesNotExist:
        return redirect("all_reports")

    if request.method == "POST":
        print("DELETING COMMENT")
        comment.delete()

    all_reports = Report.objects.all()
    context = {"reports": all_reports}
    return render(request, "all_reports.html", context)
