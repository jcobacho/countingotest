import itertools

import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2.utils import AttributeDict

SELECTION_ATTR = {'class': "form-check form-check-custom form-check-solid"}

"""
div class="form-check form-check-custom form-check-solid">
    <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault"/>
    <label class="form-check-label" for="flexCheckDefault">
        Default checkbox
    </label>
</div>

"""


class CustomCheckboxColumn(tables.columns.CheckBoxColumn):

    @property
    def header(self):
        default = {"type": "checkbox"}

        general = self.attrs.get("input")
        specific = self.attrs.get("th__input")
        attrs = AttributeDict(default, **(specific or general or {}))

        input = "<input %s/ >" % attrs.as_html()
        header_attrs = AttributeDict(SELECTION_ATTR)
        label = f"<div {header_attrs.as_html()}>{input}</div>"

        return mark_safe(label)

    def render(self, value, bound_column, record):
        input = super(CustomCheckboxColumn, self).render(value, bound_column, record)
        # include span
        attrs = AttributeDict(SELECTION_ATTR)
        label = f"<div {attrs.as_html()}>{input}</div>"

        return mark_safe(label)


class TableMixinSelection(tables.Table):
    selection = CustomCheckboxColumn(accessor="pk", attrs={'input': {'class': "form-check-input", 'autocomplete': 'off'},
                                                           'th__input': {'class': "form-check-input", 'autocomplete': 'off'}})

    class Meta:
        sequence = ('selection', '...')


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