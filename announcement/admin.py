from django.contrib import admin
from django.db.models import Count, Q

from announcement.models import CandidateTech, Candidate, Technology, Announcement

# Register your models here.


class TechItemInline(admin.StackedInline):
    model = CandidateTech
    extra = 1


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    fields = ['name', 'description']

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         _candidates_count=Count(Q(candidates__selected=True), distinct=True),
    #     )
    #     return queryset
    #
    # def total_candidates_selected(self, obj):
    #     return obj._candidates_count
    #
    # total_candidates_selected.admin_order_field = '_candidates_count'


@admin.action()
def mark_selected(self, request, queryset):
    pass
    # queryset.filter(selected=False).update(selected=True)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'ci', 'announcement', 'age', 'sex', 'get_techs')
    search_fields = ('first_name', 'last_name')
    list_filter = ('announcement', 'sex')

    fields = ['first_name', 'middle_name', 'last_name', 'ci', 'address', 'age', 'sex', 'announcement']
    # fields = ['user', 'announcement']
    inlines = [
        TechItemInline
    ]

    actions = [mark_selected]

    def get_techs(self, obj):
        return ", ".join([f'{t.tech.name} - {str(t.years_of_experience)}' for t in obj.candidatetech_set.all()])
    #
    # @admin.display(description='First Name', ordering='user__first_name')
    # def get_first_name(self, obj):
    #     return obj.user.first_name
    #
    # @admin.display(description='Last Name', ordering='user__last_name')
    # def get_last_name(self, obj):
    #     return obj.user.last_name
    #
    # @admin.display(description='CI', ordering='user__ci')
    # def get_ci(self, obj):
    #     return obj.user.ci


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    fields = ['name', 'description']

