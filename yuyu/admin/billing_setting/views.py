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
from django import shortcuts
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import views, exceptions, messages, tables, forms
from openstack_dashboard.dashboards.yuyu.cases.invoice_use_case import InvoiceUseCase
from openstack_dashboard.dashboards.yuyu.cases.setting_use_case import SettingUseCase
from openstack_dashboard.dashboards.yuyu.core.utils.price_checker import has_missing_price
from .forms import SettingForm
from .tables import SettingTable


class IndexView(tables.DataTableView):
    page_title = _("Setting")
    template_name = "admin/billing_setting/index.html"
    table_class = SettingTable

    setting_uc = SettingUseCase()

    def get_data(self):
        try:
            setting_uc = self.setting_uc.get_setting_admin(self.request)

        except Exception:
            setting_uc = []
            exceptions.handle(self.request,
                              _("Unable to retrieve data."))
        return setting_uc

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self, "table"):
            context[self.context_object_name] = self.table

        context['setting'] = self.setting_uc.get_settings(self.request)
        context['missing_price'] = has_missing_price(self.request)
        context['missing_setting'] = self.setting_uc.has_missing_setting(self.request)
        return context


class UpdateSettingView(forms.ModalFormView):
    form_class = SettingForm
    form_id = "setting_form_update"
    modal_id = "update_setting_modal"
    modal_header = _("Update Setting")
    page_title = _("Setting")
    submit_label = _("Update Setting")
    submit_url = reverse_lazy("horizon:admin:billing_setting:update_setting")
    success_url = reverse_lazy("horizon:admin:billing_setting:index")
    template_name = 'admin/billing_setting/form_setting.html'

    setting_uc = SettingUseCase()

    def get_initial(self):
        try:
            setting_uc = dict(self.setting_uc.get_setting_admin(self.request))
        except Exception:
            setting_uc = None
            exceptions.handle(self.request,
                              _("Unable to retrieve setting."))

        return setting_uc


class EnableBillingView(views.APIView):
    invoice_uc = InvoiceUseCase()

    def get(self, request, *args, **kwargs):
        try:
            self.invoice_uc.enable_billing(request)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to enable billing, Please check your price configuration"))
        return shortcuts.redirect("horizon:admin:billing_setting:index")


class DisableBillingView(views.APIView):
    invoice_uc = InvoiceUseCase()

    def get(self, request, *args, **kwargs):
        try:
            self.invoice_uc.disable_billing(request)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to disable billing"))
        return shortcuts.redirect("horizon:admin:billing_setting:index")


class ResetBillingView(views.APIView):
    invoice_uc = InvoiceUseCase()

    def get(self, request, *args, **kwargs):
        try:
            self.invoice_uc.reset_billing(request)
            messages.success(request, _("Data successfully Reset."))
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to reset billing"))
        return shortcuts.redirect("horizon:admin:billing_setting:index")
