from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    chatId = models.ForeignKey('chats.Chat', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
