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
from django import shortcuts
from django.http import HttpResponseRedirect
from django.urls import reverse
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
from ...cases.setting_use_case import SettingUseCase
from ...core.usage_cost.tables import InstanceCostTable, VolumeCostTable, FloatingIpCostTable, RouterCostTable, \
    SnapshotCostTable, ImageCostTable
from ...core.utils.invoice_utils import state_to_text


class IndexView(tables.DataTableView):
    table_class = InvoiceTable
    page_title = _("Invoice")
    template_name = "admin/projects_invoice/invoice_table.html"

    invoice_uc = InvoiceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_list'], _ = api.keystone.tenant_list(self.request, user=self.request.user.id)
        context['current_project_id'] = self.request.GET.get('project_id', self.request.user.project_id)
        context['current_project_name'] = self.request.GET.get('project_name', self.request.user.project_id)
        return context

    def get_data(self):
        project_id = self.request.GET.get('project_id', self.request.user.project_id)
        try:
            data = []
            for d in self.invoice_uc.get_simple_list(self.request, project_id):
                data.append({
                    'id': d['id'],
                    'project_id': project_id,
                    'date': formats.date_format(d['start_date'], 'd M Y'),
                    'state': state_to_text(d['state']),
                    'total': d['total_money'] or d['subtotal_money']
                })
            return list(data)
        except Exception as e:
            error_message = _('Unable to get invoice')
            exceptions.handle(self.request, error_message)
            return []


class InvoiceView(views.APIView):
    page_title = _("Invoice")

    invoice_uc = InvoiceUseCase()
    setting_uc = SettingUseCase()

    def get_template_names(self):
        if self.request.GET.get('print', None):
            return ['admin/projects_invoice/invoice_download.html']
        else:
            return ['admin/projects_invoice/invoice.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.invoice_uc.get_invoice(self.request, self.kwargs['id'], tenant_id=self.kwargs['project_id'])
        context['invoice'] = invoice
        context['setting'] = self.setting_uc.get_settings(self.request)
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


class UsageCostView(tables.MultiTableView):
    table_classes = (
        InstanceCostTable, VolumeCostTable, FloatingIpCostTable, RouterCostTable, SnapshotCostTable, ImageCostTable)
    page_title = _("Usage Cost")
    template_name = "admin/projects_invoice/cost_tables.html"

    invoice_uc = InvoiceUseCase()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.invoice = self.invoice_uc.get_invoice(self.request, self.kwargs['id'],
                                                      tenant_id=self.kwargs['project_id'])
        return super(UsageCostView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.request.invoice
        return context

    def _get_flavor_name(self, flavor_id):
        try:
            return api.nova.flavor_get(self.request, flavor_id).name
        except Exception:
            return 'Invalid Flavor'

    def _get_volume_name(self, volume_type_id):
        try:
            return api.cinder.volume_type_get(self.request, volume_type_id).name
        except Exception:
            return 'Invalid Volume'

    def get_instance_cost_data(self):
        try:
            datas = map(lambda x: {
                "id": x['id'],
                "name": x['name'],
                "flavor": self._get_flavor_name(x['flavor_id']),
                "usage": timesince(
                    dateutil.parser.isoparse(x['start_date']),
                    dateutil.parser.isoparse(x['adjusted_end_date'])
                ),
                "cost": Money(amount=x['price_charged'], currency=x['price_charged_currency'])
            }, self.request.invoice.get('instances', []))

            return datas
        except Exception:
            error_message = _('Unable to get instance cost')
            exceptions.handle(self.request, error_message)

            return []

    def get_volume_cost_data(self):
        try:
            datas = map(lambda x: {
                "id": x['id'],
                "name": x['volume_name'],
                "usage": timesince(
                    dateutil.parser.isoparse(x['start_date']),
                    dateutil.parser.isoparse(x['adjusted_end_date'])
                ),
                'type': self._get_volume_name(x['volume_type_id']),
                'size': x['space_allocation_gb'],
                "cost": Money(amount=x['price_charged'], currency=x['price_charged_currency'])
            }, self.request.invoice.get('volumes', []))
            return datas
        except Exception:
            error_message = _('Unable to get volume cost')
            exceptions.handle(self.request, error_message)

            return []

    def get_floating_ip_cost_data(self):
        try:
            datas = map(lambda x: {
                "id": x['id'],
                "name": x['ip'],
                "usage": timesince(
                    dateutil.parser.isoparse(x['start_date']),
                    dateutil.parser.isoparse(x['adjusted_end_date'])
                ),
                "cost": Money(amount=x['price_charged'], currency=x['price_charged_currency'])
            }, self.request.invoice.get('floating_ips', []))

            return datas
        except Exception:
            error_message = _('Unable to get floating ip cost')
            exceptions.handle(self.request, error_message)

            return []

    def get_router_cost_data(self):
        try:
            datas = map(lambda x: {
                "id": x['id'],
                "name": x['name'],
                "usage": timesince(
                    dateutil.parser.isoparse(x['start_date']),
                    dateutil.parser.isoparse(x['adjusted_end_date'])
                ),
                "cost": Money(amount=x['price_charged'], currency=x['price_charged_currency'])
            }, self.request.invoice.get('routers', []))

            return datas
        except Exception:
            error_message = _('Unable to get router cost')
            exceptions.handle(self.request, error_message)

            return []

    def get_snapshot_cost_data(self):
        try:
            datas = map(lambda x: {
                "id": x['id'],
                "name": x['name'],
                'size': x['space_allocation_gb'],
                "usage": timesince(
                    dateutil.parser.isoparse(x['start_date']),
                    dateutil.parser.isoparse(x['adjusted_end_date'])
                ),
                "cost": Money(amount=x['price_charged'], currency=x['price_charged_currency'])
            }, self.request.invoice.get('snapshots', []))

            return datas
        except Exception:
            error_message = _('Unable to get snapshot cost')
            exceptions.handle(self.request, error_message)

            return []

    def get_image_cost_data(self):
        try:
            datas = map(lambda x: {
                "id": x['id'],
                "name": x['name'],
                'size': x['space_allocation_gb'],
                "usage": timesince(
                    dateutil.parser.isoparse(x['start_date']),
                    dateutil.parser.isoparse(x['adjusted_end_date'])
                ),
                "cost": Money(amount=x['price_charged'], currency=x['price_charged_currency'])
            }, self.request.invoice.get('images', []))

            return datas
        except Exception:
            error_message = _('Unable to get images cost')
            exceptions.handle(self.request, error_message)

            return []


class FinishInvoice(views.APIView):
    invoice_uc = InvoiceUseCase()

    def get(self, request, *args, **kwargs):
        self.invoice_uc.finish_invoice(request, kwargs['id'])
        next_url = request.GET.get('next', reverse('horizon:admin:projects_invoice:index'))
        return HttpResponseRedirect(next_url)


class RollbackToUnpaidInvoice(views.APIView):
    invoice_uc = InvoiceUseCase()

    def get(self, request, *args, **kwargs):
        self.invoice_uc.rollback_to_unpaid_invoice(request, kwargs['id'])
        next_url = request.GET.get('next', reverse('horizon:admin:projects_invoice:index'))
        return HttpResponseRedirect(next_url)
