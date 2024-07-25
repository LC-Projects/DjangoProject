from django.db import models

# Create your models here.
class Feedback(models.Model):
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Feedback, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.subject}'