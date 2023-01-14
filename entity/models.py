from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()
# Create your models here.


class Developer(User):
    # keep class for future relationships of the developers
    class Meta(User.Meta):
        verbose_name = "Developer"
        verbose_name_plural = "Developers"


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    developers = models.ManyToManyField(Developer, related_name='teams')

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.name