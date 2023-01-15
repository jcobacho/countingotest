import django_filters


class SearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="Search", method="my_custom_filter")

    class Meta:
        fields = ("search",)

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })