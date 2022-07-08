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
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _

from horizon import views, exceptions, messages, tables, forms
from openstack_dashboard.dashboards.yuyu.cases.setting_use_case import SettingUseCase
from .forms import SettingForm
from .tables import SettingTable
from ...cases.project_overview_use_case import ProjectOverviewUseCase


class IndexView(tables.DataTableView):
    page_title = _("Setting")
    template_name = "project/billing_setting/index.html"
    table_class = SettingTable

    setting_uc = ProjectOverviewUseCase()

    def get_data(self):
        try:
            setting_uc = self.setting_uc.get_tenant(self.request)

        except Exception:
            setting_uc = []
            exceptions.handle(self.request,
                              _("Unable to retrieve data."))
        return setting_uc


class UpdateSettingView(forms.ModalFormView):
    form_class = SettingForm
    form_id = "setting_form_update"
    modal_id = "update_setting_modal"
    modal_header = _("Update Setting")
    page_title = _("Setting")
    submit_label = _("Update Setting")
    submit_url = reverse_lazy("horizon:project:billing_setting:update_setting")
    success_url = reverse_lazy("horizon:project:billing_setting:index")
    template_name = 'project/billing_setting/form_setting.html'

    setting_uc = ProjectOverviewUseCase()

    def get_initial(self):
        try:
            setting_uc = dict(self.setting_uc.get_tenant(self.request))
        except Exception:
            setting_uc = None
            exceptions.handle(self.request,
                              _("Unable to retrieve setting."))

        return setting_uc
