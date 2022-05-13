from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class DetailAction(tables.LinkAction):
    name = "detail"
    verbose_name = "Detail"

    def get_link_url(self, datum=None, *args, **kwargs):
        print(datum, args, kwargs)
        return reverse("horizon:project:invoice:download_pdf", kwargs={"id": datum['id']})


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
        row_actions = (DetailAction, )
