# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import datetime

import dateutil.parser
from dateutil.tz import tzutc
from django.template.defaultfilters import date
from django.utils.timesince import timesince
from django.utils import formats
from django.utils.translation import ugettext_lazy as _
from djmoney.money import Money

from horizon import exceptions
from horizon import tables
from horizon import views
from openstack_dashboard import api
from openstack_dashboard.dashboards.yuyu.cases.invoice_use_case import InvoiceUseCase
from .tables import InvoiceTable
from ...core.utils.invoice_utils import state_to_text


class IndexView(tables.DataTableView):
    table_class = InvoiceTable
    page_title = _("Invoice")
    template_name = "project/invoice/invoice_table.html"

    invoice_uc = InvoiceUseCase()

    def get_data(self):
        try:
            data = []
            for d in self.invoice_uc.get_simple_list(self.request):
                data.append({
                    'id': d['id'],
                    'date': formats.date_format(d['start_date'], 'M Y'),
                    'state': state_to_text(d['state']),
                    'total': d['total_money'] or d['subtotal_money']
                })
            return list(data)
        except Exception:
            error_message = _('Unable to get invoice')
            exceptions.handle(self.request, error_message)

            return []


class InvoiceView(views.APIView):
    page_title = _("Invoice")
    template_name = "project/invoice/download_pdf.html"

    invoice_uc = InvoiceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.invoice_uc.get_invoice(self.request, self.kwargs['id'])
        context['invoice'] = invoice

        context['instance_cost'] = self.get_sum_price(invoice, 'instances')
        context['volume_cost'] = self.get_sum_price(invoice, 'volumes')
        context['fip_cost'] = self.get_sum_price(invoice, 'floating_ips')
        context['router_cost'] = self.get_sum_price(invoice, 'routers')
        context['snapshot_cost'] = self.get_sum_price(invoice, 'snapshots')
        context['image_cost'] = self.get_sum_price(invoice, 'images')

        return context

    def get_sum_price(self, invoice, key):
        instance_prices = map(
            lambda x: Money(amount=x['price_charged'], currency=x['price_charged_currency']),
            invoice.get(key, [])
        )

        return sum(instance_prices)