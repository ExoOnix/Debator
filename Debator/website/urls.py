from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, PostDetailView

from . import views


urlpatterns = [
    path("", index.as_view(), name="index"),
    path("upload", views.Upload, name="upload"),
    path("p/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("p/<str:post_pk>/upvote/<int:pk>", views.UpvoteComment, name="upvote-comment"),
    path("p/<str:post_pk>/downvote/<int:pk>", views.DownvoteComment, name="downvote-post"),
    path("p/<str:post_pk>/reply/<int:pk>", views.Reply, name="reply"),
    path(
        "p/<str:post_pk>/delete/<int:pk>",
        views.DeleteComment,
        name="delete",
    ),
    path("p/<int:pk>/delete", views.DeletePost, name="delete-post"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
