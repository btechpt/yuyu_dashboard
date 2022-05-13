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

from django.conf.urls import url

from openstack_dashboard.dashboards.yuyu.admin.projects_invoice import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^invoice/pdf/(?P<project_id>[^/]+)/(?P<id>[^/]+)/$', views.InvoiceView.as_view(), name='download_pdf'),
    url(r'^invoice/usage/(?P<project_id>[^/]+)/(?P<id>[^/]+)/$', views.UsageCostView.as_view(), name='usage_cost'),
    url(r'^invoice/finish/(?P<id>[^/]+)/$', views.FinishInvoice.as_view(), name='finish_invoice'),
    url(r'^invoice/rollback_to_unpaid/(?P<id>[^/]+)/$', views.RollbackToUnpaidInvoice.as_view(),
        name='rollback_to_unpaid'),
]
