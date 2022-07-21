from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class InvoiceAction(tables.LinkAction):
    name = "invoice"
    verbose_name = "Invoice"

    def get_link_url(self, datum=None, *args, **kwargs):
        return reverse("horizon:admin:projects_invoice:invoice_detail", kwargs={
            "id": datum['id'],
            "project_id": datum['project_id'],
        })


class UsageCostAction(tables.LinkAction):
    name = "usage_cost"
    verbose_name = "Usage Cost"

    def get_link_url(self, datum=None, *args, **kwargs):
        return reverse("horizon:admin:projects_invoice:usage_cost", kwargs={
            "id": datum['id'],
            "project_id": datum['project_id'],
        })


class InvoiceTable(tables.DataTable):
    date = tables.WrappingColumn('date', verbose_name=_('Date'))
    state = tables.WrappingColumn('state', verbose_name=_('State'))
    total = tables.Column('total', verbose_name=_('Total'))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['date']

    class Meta(object):
        name = "invoice_table"
        hidden_title = True
        verbose_name = _("Invoice")
        row_actions = (InvoiceAction, UsageCostAction)
