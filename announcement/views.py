# Create your views here.
from django.views.generic import ListView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView

from announcement.filters import CandidateFilter, AnnouncementFilter
from announcement.models import Announcement, Candidate
from announcement.tables import AnnouncementTable, CandidateTable


class ListAnnouncements(SingleTableMixin, FilterView):
    template_name = 'announcement/list.html'
    table_class = AnnouncementTable
    paginate_by = 15
    model = Announcement
    filterset_class = AnnouncementFilter

    strict = False

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': "Announcements"})
        return super(ListAnnouncements, self).get_context_data(**kwargs)


class ListCandidatesView(SingleTableMixin, FilterView):
    template_name = 'announcement/candidate/list.html'
    table_class = CandidateTable
    paginate_by = 15
    model = Candidate
    filterset_class = CandidateFilter
    strict = False

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': "Candidates"})
        return super(ListCandidatesView, self).get_context_data(**kwargs)