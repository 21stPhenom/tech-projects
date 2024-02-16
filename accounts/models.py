from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ranking = models.PositiveIntegerField(verbose_name="User rank", default=0)
    projects_completed = models.PositiveIntegerField(verbose_name="Pojects Completed", default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created', '-date_updated')

    def __str__(self):
        return f"Profile for {self.user.username}"