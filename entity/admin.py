from django.contrib import admin

# Register your models here.
from entity.models import Developer


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__first_name',)

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

