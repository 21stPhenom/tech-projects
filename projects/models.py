from django.db import models
from django.contrib.postgres.fields import ArrayField
from autoslug.fields import AutoSlugField

from accounts.models import Profile

# Create your models here.
class Project(models.Model):
    difficulty_choices = {
        '0': 'beginner',
        '1': 'intermediate',
        '2': 'advanced',
        '3': 'pro'
    }

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(verbose_name='Project Description', max_length=200, unique=True)
    description = models.CharField(verbose_name='Project Description', max_length=1000)
    enrolled_profiles = models.ManyToManyField(Profile, related_name='enrolled_profiles', blank=True)
    reward = models.PositiveSmallIntegerField(verbose_name='Project Reward')
    difficulty = models.CharField(verbose_name='Project Difficulty', max_length=1, choices=difficulty_choices)
    project_slug = AutoSlugField(populate_from='name', unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created', '-date_updated')

    def __str(self):
        return f'{self.name} by {self.creator}'
    
class Solution(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='solutions')
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='projects')
    repo_link = models.URLField(verbose_name='Solution Repository', max_length=500)
    live_link = models.URLField(verbose_name='Live Solution', max_length=500)
    
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f'Solution by {self.creator.user.username}'