import itertools

import django_tables2 as tables


ACTIONS_ATTR = {"tr": {"class": "text-center"}, "td": {"class": "text-center"}}
SELECTION_ATTR = {'class': "kt-checkbox kt-checkbox--bold kt-checkbox--info"}
HEADER_ATTR = {"class": "fw-bolder text-muted"}


class TableMixinCounter(tables.Table):
    counter = tables.TemplateColumn('{{ }}', verbose_name="No")

    class Meta:
        sequence = ('counter', '...')
        # attrs = HEADER_ATTR

    def __init__(self, *args, **kwargs):
        super(TableMixinCounter, self).__init__(*args, **kwargs)
        self.count = itertools.count()

    def render_counter(self):
        return next(self.count) + 1