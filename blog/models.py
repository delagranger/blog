from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    user = models.CharField(max_length=10)
    creation_date = models.DateTimeField(auto_now_add=True)

