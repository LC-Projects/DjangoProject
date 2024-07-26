from django.db import models, migrations
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # super().save(*args, **kwargs)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


# Create your models here.
class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat.name}-{self.created_at}"


class Chat(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat.name}-{self.user.username}"
