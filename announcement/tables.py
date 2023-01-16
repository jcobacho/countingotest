import django_tables2 as tables

# from core.tableMixins import TableMixinSelection

from announcement.models import Announcement, Candidate
from core.tables import TableMixinCounter, TableMixinSelection


class AnnouncementTable(TableMixinCounter):
    actions = tables.columns.TemplateColumn(
        verbose_name="Actions", template_name="announcement/table_actions.html", orderable=False
    )

    class Meta(TableMixinCounter.Meta):
        model = Announcement
        fields = ("counter", "name", "actions")


class CandidateTable(TableMixinSelection):
    actions = tables.columns.TemplateColumn(
        verbose_name="Actions", template_name="announcement/candidate/table_actions.html", orderable=False
    )

    tech_years = tables.columns.TemplateColumn(
        verbose_name="Tech-Years", template_name="announcement/candidate/table_tech_years.html", orderable=False
    )

    class Meta:
        model = Candidate
        fields = ("selection", "announcement", "first_name", "ci", "sex", "age", "tech_years", "actions")
