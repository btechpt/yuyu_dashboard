from horizon import exceptions, tables, tabs
from openstack_dashboard.dashboards.yuyu.admin.price_configuration.tables import FlavorPriceTable, VolumePriceTable, \
    FloatingIpPriceTable, RouterPriceTable, SnapshotPriceTable, ImagePriceTable
from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.dashboards.yuyu.cases.flavor_price_use_case import FlavorPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.floating_ip_price_use_case import FloatingIpPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.volume_price_use_case import VolumePriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.router_price_use_case import RouterPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.snapshot_price_use_case import SnapshotPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.image_price_use_case import ImagePriceUseCase


class FlavorTab(tabs.TableTab):
    table_classes = (FlavorPriceTable,)
    name = _("Flavor")
    slug = "flavor"
    template_name = 'horizon/common/_detail_table.html'

    flavor_price_uc = FlavorPriceUseCase()

    def get_flavor_price_data(self):
        try:
            data = self.flavor_price_uc.list(self.request)
            return data
        except Exception:
            error_message = _('Unable to get flavor prices')
            exceptions.handle(self.request, error_message)

            return []


class VolumeTab(tabs.TableTab):
    table_classes = (VolumePriceTable,)
    name = _("Volume")
    slug = "volume"
    template_name = 'horizon/common/_detail_table.html'

    volume_price_uc = VolumePriceUseCase()

    def get_volume_price_data(self):
        try:
            data = self.volume_price_uc.list(self.request)
            return data
        except Exception:
            error_message = _('Unable to get volume prices')
            exceptions.handle(self.request, error_message)

            return []


class FloatingIpTab(tabs.TableTab):
    table_classes = (FloatingIpPriceTable,)
    name = _("Floating IP")
    slug = "floating_ip"
    template_name = 'horizon/common/_detail_table.html'

    fip_price_uc = FloatingIpPriceUseCase()

    def get_floating_ip_price_data(self):
        try:
            data = self.fip_price_uc.list(self.request)
            return data
        except Exception:
            error_message = _('Unable to get floating IP prices')
            exceptions.handle(self.request, error_message)

            return []


class RouterTab(tabs.TableTab):
    table_classes = (RouterPriceTable,)
    name = _("Router")
    slug = "router"
    template_name = 'horizon/common/_detail_table.html'

    price_uc = RouterPriceUseCase()

    def get_router_price_data(self):
        try:
            data = self.price_uc.list(self.request)
            return data
        except Exception:
            error_message = _('Unable to get router prices')
            exceptions.handle(self.request, error_message)

            return []


class SnapshotTab(tabs.TableTab):
    table_classes = (SnapshotPriceTable,)
    name = _("Snapshot")
    slug = "snapshot"
    template_name = 'horizon/common/_detail_table.html'

    price_uc = SnapshotPriceUseCase()

    def get_snapshot_price_data(self):
        try:
            data = self.price_uc.list(self.request)
            return data
        except Exception:
            error_message = _('Unable to get snapshot prices')
            exceptions.handle(self.request, error_message)

            return []

class ImageTab(tabs.TableTab):
    table_classes = (ImagePriceTable,)
    name = _("Image")
    slug = "image"
    template_name = 'horizon/common/_detail_table.html'

    price_uc = ImagePriceUseCase()

    def get_image_price_data(self):
        try:
            data = self.price_uc.list(self.request)
            return data
        except Exception:
            error_message = _('Unable to get image prices')
            exceptions.handle(self.request, error_message)

            return []


class PriceConfigurationTabs(tabs.TabGroup):
    slug = "price_config"
    tabs = (FlavorTab, VolumeTab, FloatingIpTab, RouterTab, SnapshotTab, ImageTab, )
    sticky = True
