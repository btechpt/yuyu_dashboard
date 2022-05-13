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

from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from neutronclient.common import exceptions as neutron_exc

from horizon import exceptions, tabs
from horizon import forms
from openstack_dashboard import api
from openstack_dashboard.dashboards.yuyu.cases.flavor_price_use_case import FlavorPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.floating_ip_price_use_case import FloatingIpPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.volume_price_use_case import VolumePriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.router_price_use_case import RouterPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.snapshot_price_use_case import SnapshotPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.image_price_use_case import ImagePriceUseCase
from .forms import FlavorPriceForm, VolumePriceForm, FloatingIpPriceForm, RouterPriceForm, SnapshotPriceForm, ImagePriceForm
from .tabs import PriceConfigurationTabs
from ...core.utils.price_checker import has_missing_price


class IndexView(tabs.TabbedTableView):

    tab_group_class = PriceConfigurationTabs
    page_title = _("Price Configuration")
    template_name = "admin/price_configuration/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['missing_price'] = has_missing_price(self.request)

        return context


class FlavorPriceAddFormView(forms.ModalFormView):
    form_class = FlavorPriceForm
    form_id = "flavor_price_form"
    page_title = _("Create Flavor Price")
    submit_label = _("Create Flavor Price")
    submit_url = reverse_lazy("horizon:admin:price_configuration:flavor_price_create")
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_flavor.html'

    flavor_price_uc = FlavorPriceUseCase()

    def get_object_display(self, obj):
        return obj.flavor_id

    def get_initial(self):
        added_ids = []
        flavors = []
        try:
            added_ids = map(lambda x: x['flavor_id'], self.flavor_price_uc.list(self.request))
            flavors = api.nova.flavor_list(self.request)
        except neutron_exc.ConnectionFailed:
            exceptions.handle(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve flavors."))

        flavor_list = []
        for flavor in flavors:
            if flavor.id not in added_ids:
                flavor_list.append((flavor.id, flavor.name))

        if not flavor_list:
            flavor_list = [(None, _("No flavors available"))]
        return {'flavor_list': flavor_list}


class FlavorPriceUpdateFormView(forms.ModalFormView):
    form_class = FlavorPriceForm
    form_id = "flavor_price_form_update"
    page_title = _("Flavor Price")
    submit_label = _("Update Flavor Price")
    submit_url = "horizon:admin:price_configuration:flavor_price_update"
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_flavor.html'

    flavor_price_uc = FlavorPriceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_object_display(self, obj):
        return obj.flavor_id

    def get_initial(self):
        try:
            flavor_price = self.flavor_price_uc.get(self.request, self.kwargs['id'])
        except Exception:
            flavor_price = None
            exceptions.handle(self.request,
                              _("Unable to retrieve flavor price."))

        return {
            'model_id': flavor_price['id'],
            'flavor_list': [(flavor_price['flavor_id'], flavor_price['name'])],
            'hourly_price': flavor_price['hourly_price'],
            'monthly_price': flavor_price['monthly_price']
        }


class VolumePriceAddFormView(forms.ModalFormView):
    form_class = VolumePriceForm
    form_id = "volume_price_form"
    page_title = _("Create Volume Price")
    submit_label = _("Create Volume Price")
    submit_url = reverse_lazy("horizon:admin:price_configuration:volume_price_create")
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_volume.html'

    volume_price_uc = VolumePriceUseCase()

    def get_object_display(self, obj):
        return obj.volume_type_id

    def get_initial(self):
        added_ids = []
        volumes = []
        try:
            added_ids = map(lambda x: x['volume_type_id'], self.volume_price_uc.list(self.request))
            volumes = api.cinder.volume_type_list(self.request)
        except neutron_exc.ConnectionFailed:
            exceptions.handle(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve volumes."))

        volume_list = []
        for d in volumes:
            if d.id not in added_ids:
                volume_list.append((d.id, d.name))

        if not volume_list:
            volume_list = [(None, _("No volume type available"))]
        return {'volume_type_list': volume_list}


class VolumePriceUpdateFormView(forms.ModalFormView):
    form_class = VolumePriceForm
    form_id = "volume_price_form_update"
    page_title = _("Volume Price")
    submit_label = _("Update Volume Price")
    submit_url = "horizon:admin:price_configuration:volume_price_update"
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_volume.html'

    volume_price_uc = VolumePriceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_object_display(self, obj):
        return obj.volume_type_id

    def get_initial(self):
        try:
            volume = self.volume_price_uc.get(self.request, self.kwargs['id'])
        except Exception:
            volume = None
            exceptions.handle(self.request,
                              _("Unable to retrieve volume price."))

        return {
            'model_id': volume['id'],
            'volume_type_list': [(volume['volume_type_id'], volume['name'])],
            'hourly_price': volume['hourly_price'],
            'monthly_price': volume['monthly_price']
        }



class FloatingIpPriceAddFormView(forms.ModalFormView):
    form_class = FloatingIpPriceForm
    form_id = "floating_ip_price_form"
    page_title = _("Create Floating IP Price")
    submit_label = _("Create Floating IP Price")
    submit_url = reverse_lazy("horizon:admin:price_configuration:floating_ip_price_create")
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_floating_ip.html'

    def get_object_display(self, obj):
        return obj.id


class FloatingIpPriceUpdateFormView(forms.ModalFormView):
    form_class = FloatingIpPriceForm
    form_id = "floating_ip_price_form_update"
    page_title = _("Floating IP Price")
    submit_label = _("Update Floating IP Price")
    submit_url = "horizon:admin:price_configuration:floating_ip_price_update"
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_floating_ip.html'

    fip_price_uc = FloatingIpPriceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_object_display(self, obj):
        return obj.id

    def get_initial(self):
        try:
            volume = self.fip_price_uc.get(self.request, self.kwargs['id'])
        except Exception:
            volume = None
            exceptions.handle(self.request,
                              _("Unable to retrieve floating ip price."))

        return {
            'model_id': volume['id'],
            'hourly_price': volume['hourly_price'],
            'monthly_price': volume['monthly_price']
        }


class RouterPriceAddFormView(forms.ModalFormView):
    form_class = RouterPriceForm
    form_id = "router_price_form"
    page_title = _("Create Router Price")
    submit_label = _("Create Router Price")
    submit_url = reverse_lazy("horizon:admin:price_configuration:router_price_create")
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_router.html'

    def get_object_display(self, obj):
        return obj.id


class RouterPriceUpdateFormView(forms.ModalFormView):
    form_class = RouterPriceForm
    form_id = "router_price_form_update"
    page_title = _("Router Price")
    submit_label = _("Update Router Price")
    submit_url = "horizon:admin:price_configuration:router_price_update"
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_router.html'

    price_uc = RouterPriceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_object_display(self, obj):
        return obj.id

    def get_initial(self):
        try:
            volume = self.price_uc.get(self.request, self.kwargs['id'])
        except Exception:
            volume = None
            exceptions.handle(self.request,
                              _("Unable to retrieve router price."))

        return {
            'model_id': volume['id'],
            'hourly_price': volume['hourly_price'],
            'monthly_price': volume['monthly_price']
        }


class SnapshotPriceAddFormView(forms.ModalFormView):
    form_class = SnapshotPriceForm
    form_id = "snapshot_form"
    page_title = _("Create Snapshot Price")
    submit_label = _("Create Snapshot Price")
    submit_url = reverse_lazy("horizon:admin:price_configuration:snapshot_price_create")
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_snapshot.html'

    def get_object_display(self, obj):
        return obj.id


class SnapshotPriceUpdateFormView(forms.ModalFormView):
    form_class = SnapshotPriceForm
    form_id = "snapshot_form_update"
    page_title = _("Snapshot Price")
    submit_label = _("Update Snapshot Price")
    submit_url = "horizon:admin:price_configuration:snapshot_price_update"
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_snapshot.html'

    price_uc = SnapshotPriceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_object_display(self, obj):
        return obj.id

    def get_initial(self):
        try:
            volume = self.price_uc.get(self.request, self.kwargs['id'])
        except Exception:
            volume = None
            exceptions.handle(self.request,
                              _("Unable to retrieve snapshot price."))

        return {
            'model_id': volume['id'],
            'hourly_price': volume['hourly_price'],
            'monthly_price': volume['monthly_price']
        }


class ImagePriceAddFormView(forms.ModalFormView):
    form_class = ImagePriceForm
    form_id = "snapshot_form"
    page_title = _("Create Image Price")
    submit_label = _("Create Image Price")
    submit_url = reverse_lazy("horizon:admin:price_configuration:image_price_create")
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_image.html'

    def get_object_display(self, obj):
        return obj.id


class ImagePriceUpdateFormView(forms.ModalFormView):
    form_class = ImagePriceForm
    form_id = "image_form_update"
    page_title = _("Image Price")
    submit_label = _("Update Image Price")
    submit_url = "horizon:admin:price_configuration:image_price_update"
    success_url = reverse_lazy("horizon:admin:price_configuration:index")
    template_name = 'admin/price_configuration/create_image.html'

    price_uc = ImagePriceUseCase()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_object_display(self, obj):
        return obj.id

    def get_initial(self):
        try:
            volume = self.price_uc.get(self.request, self.kwargs['id'])
        except Exception:
            volume = None
            exceptions.handle(self.request,
                              _("Unable to retrieve image price."))

        return {
            'model_id': volume['id'],
            'hourly_price': volume['hourly_price'],
            'monthly_price': volume['monthly_price']
        }
