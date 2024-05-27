from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Count

import filetype

# Reccomendations
import pandas as pd
import numpy as np
import scipy.stats

from .models import Post, Comment, Attachment, PosVote
from .forms import UploadForm, CommentForm


class index(ListView):
    model = Post
    paginate_by = 100
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            object_list = Post.objects.filter(title__icontains=search).order_by('-created_at')
        else:
            object_list = Post.objects.all().order_by("-created_at")
        return object_list


class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = "post_detail.html"
    form_class = CommentForm

    def get_success_url(self):
        return redirect(".")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm(initial={"post": self.object})

        # Retrieve comments and annotate them with the count of upvotes
        comments = (
            Comment.objects.filter(parent_post__pk=self.kwargs["pk"])
            .annotate(num_votes=(Count("upvote") - Count("downvote")))
            .order_by("-num_votes")
        )

        context["comments"] = comments

        # Calculate reaction counts for each position
        positions = self.object.get_position()
        reaction_counts = {
            position: PosVote.objects.filter(position=position).count()
            for position in positions
        }
        context["reaction_counts"] = reaction_counts

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        print(form.cleaned_data, self.request.POST.get("position"))
        comment_instance = Comment(
            content=form.cleaned_data["content"],
            author=self.request.user,
            parent_post=Post.objects.get(pk=self.kwargs["pk"]),
            position=self.request.POST.get("position"),
        )

        comment_instance.save()
        return HttpResponseRedirect(
            f"/p/{self.kwargs['pk']}"
        )


def Upload(request):
    if request.user.has_perm("website.add_post"):
        if request.method == "POST":
            form = UploadForm(request.POST, request.FILES)
            print(form.errors.as_text)
            if form.is_valid():
                post_instance = Post(
                    title=form.cleaned_data["title"],
                    content=form.cleaned_data["content"],
                    author=request.user,
                )
                post_instance.set_position(form.cleaned_data["positions"].split(","))
                post_instance.save()
                print("cleaned data", form.cleaned_data)

                if len(form.cleaned_data["attachments"]) > 0:
                    files = form.cleaned_data["attachments"]
                    for f in files:
                        if "image" in filetype.guess(f).mime:
                            attachment_instance = Attachment(
                                parent_post=post_instance,
                                image=f
                            )
                            attachment_instance.save()
                        if "video" in filetype.guess(f).mime:
                            attachment_instance = Attachment(
                                parent_post=post_instance,
                                video=f
                            )
                            attachment_instance.save()
                return HttpResponseRedirect(f"/p/{post_instance.pk}")

        # if a GET (or any other method) we'll create a blank form
        else:
            form = UploadForm()
        return render(request, "upload.html", {"form": UploadForm})
    else:
        raise PermissionDenied


def Reply(request, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)

            if form.is_valid():
                print(form.cleaned_data, kwargs["post_pk"], kwargs["pk"])
                comment_instance = Comment(
                    content=form.cleaned_data["content"],
                    author=request.user,
                    parent_post=Post.objects.get(pk=kwargs['post_pk']),
                    parent_comment=Comment.objects.get(pk=kwargs["pk"]),
                )

                comment_instance.save()
                return redirect(
                    f"/p/{kwargs['post_pk']}"
                )
        else:
            redirect("/")
    else:
        raise PermissionDenied


def DeleteComment(request, **kwargs):
    if request.user.is_authenticated:
        if request.user.pk == Comment.objects.get(pk=kwargs["pk"]).author.pk or request.user.is_superuser == True:
            Comment.objects.get(pk=kwargs["pk"]).delete()
            return redirect(f"/p/{kwargs['post_pk']}")
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def DeletePost(request, **kwargs):
    if request.user.is_authenticated:
        if request.user.has_perm("website.delete_post"):
            Post.objects.get(pk=kwargs["pk"]).delete()
            return redirect(f"/")
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def UpvoteComment(request, **kwargs):
    if request.user.is_authenticated:
        if not request.user.comment_downvotes.filter(pk=kwargs["pk"]).exists():

            if request.user.comment_upvotes.filter(pk=kwargs["pk"]).exists():
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.upvote.remove(request.user)
                comment.save()
            else:
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.upvote.add(request.user)
                comment.save()
        return redirect(f"/p/{kwargs['post_pk']}")
    else:
        raise PermissionDenied


def DownvoteComment(request, **kwargs):
    if request.user.is_authenticated:
        if not request.user.comment_upvotes.filter(pk=kwargs["pk"]).exists():
            if request.user.comment_downvotes.filter(pk=kwargs["pk"]).exists():
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.downvote.remove(request.user)
                comment.save()
            else:
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.downvote.add(request.user)
                comment.save()
        return redirect(f"/p/{kwargs['post_pk']}")
    else:
        raise PermissionDenied


def AddVote(request, **kwargs):
    if request.user.is_authenticated:
        if not PosVote.objects.filter(post=Post.objects.get(pk=kwargs["post_pk"]), author=request.user):
            vote = PosVote(
                author=request.user,
                post=Post.objects.get(pk=kwargs["post_pk"]),
                position=kwargs["pos"],
            )
            vote.save()
        else:
            vote = PosVote.objects.get(post=Post.objects.get(pk=kwargs["post_pk"]), author=request.user)
            vote.delete()
        return redirect(f"/p/{kwargs['post_pk']}")
    else:
        raise PermissionDenied
