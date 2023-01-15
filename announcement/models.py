from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Announcement(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse("announcement_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("announcement-detail", kwargs={"pk": self.pk})

    @property
    def total_candidates(self):
        return self.candidates.filter(selected=True).count()


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name


class Candidate(User):

    techs = models.ManyToManyField(Technology, through='CandidateTech')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='candidates')

    class Meta(User.Meta):
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def get_edit_url(self):
        return reverse("candidate_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("candidate-detail", kwargs={"pk": self.pk})


class CandidateTech(models.Model):
    tech = models.ForeignKey(Technology, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    years_of_experience = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = 'Technologies'
        unique_together = ('candidate', 'tech')

    def __str__(self):
        return f'{self.tech.__str__()} {self.years_of_experience}'
