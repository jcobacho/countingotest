# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView

from announcement.filters import CandidateFilter, AnnouncementFilter
from announcement.forms import AnnouncementForm
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


class CreateAnnouncementView(CreateView):
    template_name = 'announcement/form.html'
    form_class = AnnouncementForm
    success_url = reverse_lazy('announcement_list')


class UpdateAnnouncementView(UpdateView):
    template_name = 'announcement/form.html'
    form_class = AnnouncementForm
    success_url = reverse_lazy('announcement_list')
    model = Announcement


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