from django import forms

from announcement.models import Announcement, Candidate


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


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ['first_name', 'middle_name', 'last_name', 'ci', 'address', 'age', 'sex', 'announcement']
