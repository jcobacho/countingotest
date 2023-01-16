from django import forms
from django.contrib.auth import get_user_model

from announcement.models import Announcement, Candidate
User = get_user_model()


class AnnouncementForm(forms.ModelForm):
    """
    Form for the model Announcement.

    """

    class Meta:
        model = Announcement
        fields = (
            "name",
            "description",
        )


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'ci', 'address', 'age', 'sex']


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ['announcement']
