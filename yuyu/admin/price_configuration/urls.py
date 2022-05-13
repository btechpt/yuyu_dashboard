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

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^flavor_price/create/$', views.FlavorPriceAddFormView.as_view(), name='flavor_price_create'),
    url(r'^flavor_price/update/(?P<id>[^/]+)/$', views.FlavorPriceUpdateFormView.as_view(), name='flavor_price_update'),
    url(r'^volume_price/create/$', views.VolumePriceAddFormView.as_view(), name='volume_price_create'),
    url(r'^volume_price/update/(?P<id>[^/]+)/$', views.VolumePriceUpdateFormView.as_view(), name='volume_price_update'),
    url(r'^floating_ip_price/create/$', views.FloatingIpPriceAddFormView.as_view(), name='floating_ip_price_create'),
    url(r'^floating_ip_price/update/(?P<id>[^/]+)/$', views.FloatingIpPriceUpdateFormView.as_view(),
        name='floating_ip_price_update'),
    url(r'^router_price/create/$', views.RouterPriceAddFormView.as_view(), name='router_price_create'),
    url(r'^router_price/update/(?P<id>[^/]+)/$', views.RouterPriceUpdateFormView.as_view(),
        name='router_price_update'),
    url(r'^snapshot_price/create/$', views.SnapshotPriceAddFormView.as_view(), name='snapshot_price_create'),
    url(r'^snapshot_price/update/(?P<id>[^/]+)/$', views.SnapshotPriceUpdateFormView.as_view(),
        name='snapshot_price_update'),
    url(r'^image_price/create/$', views.ImagePriceAddFormView.as_view(), name='image_price_create'),
    url(r'^image_price/update/(?P<id>[^/]+)/$', views.ImagePriceUpdateFormView.as_view(),
        name='image_price_update'),
]
