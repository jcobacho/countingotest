import django_filters
from django.db.models import Q

from announcement.models import Candidate, Technology
from core.filters import SearchFilter


class AnnouncementFilter(SearchFilter):

    class Meta:
        model = Candidate
        fields = ("search",)

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class CandidateFilter(SearchFilter):
    technology = django_filters.ModelChoiceFilter(label=Technology._meta.verbose_name,
                                              queryset=Technology.objects.all(), method='tech_filter')

    class Meta:
        model = Candidate
        fields = ("search", "technology")

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value)
                               | Q(middle_name__icontains=value)
                               | Q(last_name__icontains=value)
                               )

    def tech_filter(self, queryset, name, instance):

        return queryset.filter(techs__id=instance.id).order_by('-candidatetech__years_of_experience')