from django import forms
from announcement.models import Announcement


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
