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
import json

from django import shortcuts
from django.utils.translation import ugettext_lazy as _

from horizon import views
from openstack_dashboard.dashboards.yuyu.cases.admin_overview_use_case import AdminOverviewUseCase


class IndexView(views.APIView):
    page_title = _("Billing Overview")
    template_name = "admin/billing_overview/index.html"

    overview_uc = AdminOverviewUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_resource_json'] = json.dumps(self.overview_uc.total_resource(self.request))
        context['active_resource_json'] = json.dumps(self.overview_uc.active_resource(self.request))
        context['price_total_resource_json'] = json.dumps(self.overview_uc.price_total_resource(self.request))
        context['price_active_resource_json'] = json.dumps(self.overview_uc.price_active_resource(self.request))

        return context
