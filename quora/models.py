from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    typeChoice = (
        ("Public", "PUBLIC"),
        ("Limited", "LIMITED"),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, choices=typeChoice, default="Public")
    active = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username} -> Question No {str(self.id)}"


class Comment(models.Model):
    text = models.TextField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username} -> Question No {str(self.message.id)}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> Answer No {str(self.comment.id)}"


class MessageLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message_like")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> Answer No {str(self.message.id)}"
