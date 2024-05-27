from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
import json

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    positions = models.CharField(max_length=1000, default=json.dumps(["Pro", "Against"]))

    def set_position(self, lst):
        self.positions = json.dumps(lst)
    def get_position(self):
        return json.loads(self.positions)

    def __str__(self):
        return self.title

class PosVote(models.Model):
    position = models.CharField(max_length=1000)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reaction")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")

    def __str__(self):
        return self.position

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="children")
    created_at = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(User, related_name="comment_upvotes", blank=True)
    downvote = models.ManyToManyField(User, related_name="comment_downvotes", blank=True)
    position = models.CharField(max_length=1000, default="Pro")
    @property
    def upvotes_count(self):
        return self.upvote.count() - self.downvote.count()
    def __str__(self):
        return str(self.upvote.count() - self.downvote.count())


class Attachment(models.Model):
    image = models.ImageField(upload_to="attachments/", null=True, default=None)
    video = models.FileField(upload_to="attachments/", null=True, default=None)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachments")

    def clean(self):
        if self.video and self.image:
            raise ValidationError("Please select only a video OR an image, not both.")
    def __str__(self):
        return str(self.parent_post)
