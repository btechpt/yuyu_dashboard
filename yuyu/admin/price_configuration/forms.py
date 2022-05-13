from django.utils.translation import ugettext_lazy as _

from horizon import forms
from openstack_dashboard.dashboards.yuyu.cases.flavor_price_use_case import FlavorPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.floating_ip_price_use_case import FloatingIpPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.router_price_use_case import RouterPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.snapshot_price_use_case import SnapshotPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.volume_price_use_case import VolumePriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.image_price_use_case import ImagePriceUseCase
from openstack_dashboard.dashboards.yuyu.core.pricing_admin.forms import BasePriceForm


class FlavorPriceForm(BasePriceForm):
    flavor = forms.ThemableChoiceField(label=_("Flavor"))

    USE_CASE = FlavorPriceUseCase()
    NAME = "Flavor Price"

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        flavor_list = kwargs.get('initial', {}).get('flavor_list', [])
        self.fields['flavor'].choices = flavor_list

    def to_payload(self, data):
        payload = super().to_payload(data)
        payload["flavor_id"] = data["flavor"]

        return payload


class VolumePriceForm(BasePriceForm):
    volume_type = forms.ThemableChoiceField(label=_("Volume Type"))

    USE_CASE = VolumePriceUseCase()
    NAME = "Volume Price"

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        volume_type_list = kwargs.get('initial', {}).get('volume_type_list', [])
        self.fields['volume_type'].choices = volume_type_list

    def to_payload(self, data):
        payload = super().to_payload(data)
        payload["volume_type_id"] = data["volume_type"]

        return payload


class FloatingIpPriceForm(BasePriceForm):
    USE_CASE = FloatingIpPriceUseCase()
    NAME = "Floating IP Price"


class RouterPriceForm(BasePriceForm):
    USE_CASE = RouterPriceUseCase()
    NAME = "Router Price"


class SnapshotPriceForm(BasePriceForm):
    USE_CASE = SnapshotPriceUseCase()
    NAME = "Snapshot Price"

class ImagePriceForm(BasePriceForm):
    USE_CASE = ImagePriceUseCase()
    NAME = "Image Price"
