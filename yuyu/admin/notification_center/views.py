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
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions, tables, views
from openstack_dashboard import api
from .tables import NotificationTable
from ...cases.notification_use_case import NotificationCenterUseCase


class IndexView(tables.DataTableView):
    page_title = _("Notification Center")
    template_name = "admin/notification_center/index.html"
    table_class = NotificationTable

    notification_uc = NotificationCenterUseCase()

    def get_data(self):
        filter_selection = self.request.GET.get('tenant_id', None)
        try:
            notification_uc = self.notification_uc.get_list(self.request, filter_selection)
        except Exception:
            notification_uc = []
            exceptions.handle(self.request,
                              _("Unable to retrieve data."))
        return notification_uc

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self, "table"):
            context[self.context_object_name] = self.table

        context['select_list'], _ = api.keystone.tenant_list(self.request, user=self.request.user.id)
        context['current_tenant_id'] = self.request.GET.get('tenant_id', None)

        return context


class DetailView(views.APIView):
    page_title = _("Notification Detail")
    template_name = "admin/notification_center/notification_detail.html"
    notification_uc = NotificationCenterUseCase()

    def get_data(self, request, context, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        notification_uc = self.notification_uc.get_detail(self.request,
                                                          notification_id=self.kwargs['notification_id'])
        context['notification'] = notification_uc
        return context


class ReadAllView(views.APIView):
    notification_uc = NotificationCenterUseCase()

    def get(self, request, *args, **kwargs):
        try:
            notifications = self.notification_uc.get_list(self.request,
                                                          filter_selection=self.kwargs['selection'])
            for n in notifications:
                if not n["is_read"]:
                    self.notification_uc.set_read(request, n['id'])
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to mark read All Notification, Please contact admin"))
        return shortcuts.redirect("horizon:admin:notification_center:index")


class ResendView(views.APIView):
    notification_uc = NotificationCenterUseCase()

    def get(self, request, *args, **kwargs):
        try:
            notification_id = self.kwargs['notification_id']

            self.notification_uc.set_resend(request, notification_id)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to Resend Notification, Please contact admin"))
        return shortcuts.redirect("horizon:admin:notification_center:index")
