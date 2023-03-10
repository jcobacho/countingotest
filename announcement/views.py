# Create your views here.
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView
from django_tables2.export import ExportMixin

from announcement.filters import CandidateFilter, AnnouncementFilter
from announcement.forms import AnnouncementForm, CandidateForm, UserForm
from announcement.models import Announcement, Candidate, CandidateTech
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


class ListCandidatesView(ExportMixin, SingleTableMixin, FilterView):
    template_name = 'announcement/candidate/list.html'
    table_class = CandidateTable
    paginate_by = 15
    model = Candidate
    filterset_class = CandidateFilter
    strict = False
    exclude_columns = ("selection", "actions")
    dataset_kwargs = {"title": "Candidates"}

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': "Candidates"})
        return super(ListCandidatesView, self).get_context_data(**kwargs)


class CreateCandidateView(CreateView):
    template_name = 'announcement/candidate/form.html'
    form_class = CandidateForm
    form_class2 = UserForm
    formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'),
                                          min_num=1, validate_min=True, extra=0, can_delete=False)

    success_url = reverse_lazy('candidate_list')

    def post(self, request, *args, **kwargs):

        self.object = None

        formset = self.get_formset()
        form = self.get_form()
        form2 = self.get_form(form_class=self.form_class2)

        if form.is_valid() and form2.is_valid() and formset.is_valid():
            return self.form_valid(form, form2, formset)
        else:
            return self.form_invalid(form, form2, formset)

    def get_formset(self):
        formset = self.formset_class(**self.get_formset_kwargs())
        return formset

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {}

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = self.get_formset()

        if 'form2' not in kwargs:
            kwargs['form2'] = self.get_form(form_class=self.form_class2)

        return super(CreateCandidateView, self).get_context_data(**kwargs)

    def form_valid(self, form, form2, formset):

        user_instance = form2.save()
        self.object = form.save(commit=False)
        self.object.user = user_instance
        self.object.save()
        formset.instance = self.object
        formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, form2, formset):

        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, form2=form2, formset=formset))


class UpdateCandidateView(UpdateView):
    template_name = 'announcement/candidate/form.html'
    form_class = CandidateForm
    form_class2 = UserForm
    formset_class = inlineformset_factory(Candidate, CandidateTech, fields=('tech', 'years_of_experience'), extra=0,
                                          min_num=1, validate_min=True, can_delete=True)
    queryset = Candidate.objects.all()
    success_url = reverse_lazy('candidate_list')

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        formset = self.get_formset()
        form = self.get_form()
        form2 = self.get_form2()

        if form.is_valid() and form2.is_valid() and formset.is_valid():
            return self.form_valid(form, form2, formset)
        else:
            return self.form_invalid(form, form2, formset)

    def get_formset(self):
        formset = self.formset_class(**self.get_formset_kwargs())
        return formset

    def get_form2_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object.user:
            kwargs.update({'instance': self.object.user})
        return kwargs

    def get_form2(self):
        return self.form_class2(**self.get_form2_kwargs())

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {}

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = self.get_formset()

        if 'form2' not in kwargs:
            kwargs['form2'] = self.get_form2()

        return super(UpdateCandidateView, self).get_context_data(**kwargs)

    def form_valid(self, form, form2, formset):

        form2.save()
        self.object = form.save()
        formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, form2, formset):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, form2=form2, formset=formset))

