from django.utils.translation import ugettext_lazy as _

from horizon import tables
from openstack_dashboard.dashboards.yuyu.cases.flavor_price_use_case import FlavorPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.floating_ip_price_use_case import FloatingIpPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.volume_price_use_case import VolumePriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.router_price_use_case import RouterPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.snapshot_price_use_case import SnapshotPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.image_price_use_case import ImagePriceUseCase
from openstack_dashboard.dashboards.yuyu.core.pricing_admin.tables import BasePriceTable, BaseCreatePrice, \
    BaseEditPrice, BaseDeletePrice


def create_create_action(type_name, **kwargs):
    return type(type_name, (BaseCreatePrice,), kwargs)


def create_filter_action(type_name, **kwargs):
    return type(type_name, (tables.FilterAction,), kwargs)


def create_edit_action(type_name, **kwargs):
    return type(type_name, (BaseEditPrice,), kwargs)


def create_delete_action(type_name, **kwargs):
    return type(type_name, (BaseDeletePrice,), kwargs)


class FlavorPriceTable(BasePriceTable):
    name = tables.WrappingColumn('name', verbose_name=_('Flavor Name'))

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "flavor_price"
        verbose_name = _("Flavor Price")
        table_actions = (
            create_filter_action(
                type_name="FlavorPriceFilter",
                name="flavor_price_filter"
            ),
            create_create_action(
                type_name="FlavorPriceCreate",
                name="flavor_price_create",
                verbose_name=_("Create Flavor Price"),
                url="horizon:admin:price_configuration:flavor_price_create"
            )
        )
        row_actions = (
            create_edit_action(
                type_name="FlavorPriceUpdate",
                name="flavor_price_edit",
                verbose_name=_("Edit Flavor Price"),
                url="horizon:admin:price_configuration:flavor_price_update"
            ),
            create_delete_action(
                type_name="FlavorPriceDelete",
                use_case=FlavorPriceUseCase(),
                single_action_label="Flavor Price",
                plural_action_label="Flavor Prices"
            )
        )


class VolumePriceTable(BasePriceTable):
    name = tables.WrappingColumn('name', verbose_name=_('Volume Type Name'))

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "volume_price"
        verbose_name = _("Volume Price")
        table_actions = (
            create_filter_action(
                type_name="VolumePriceFilter",
                name="volume_price_filter"
            ),
            create_create_action(
                type_name="VolumePriceCreate",
                name="create_volume_price",
                verbose_name=_("Create Volume Price"),
                url="horizon:admin:price_configuration:volume_price_create"
            )
        )
        row_actions = (
            create_edit_action(
                type_name="VolumePriceEdit",
                name="update_volume_price",
                verbose_name=_("Edit Volume Price"),
                url="horizon:admin:price_configuration:volume_price_update"
            ),
            create_delete_action(
                type_name="VolumePriceDelete",
                use_case=VolumePriceUseCase(),
                single_action_label="Volume Price",
                plural_action_label="Volume Prices"
            )
        )


class FloatingIpPriceTable(BasePriceTable):
    def get_object_display(self, datum):
        return datum['id']

    class Meta(object):
        name = "floating_ip_price"
        verbose_name = _("Floating IP Price")
        table_actions = (
            create_filter_action(
                type_name="FloatingIpPriceFilter",
                name="floating_ip_price_filter"
            ),
            create_create_action(
                type_name="FloatingIpPriceCreate",
                name="create_floating_ip_price",
                verbose_name=_("Create Floating IP Price"),
                url="horizon:admin:price_configuration:floating_ip_price_create",
                single_data=True,
            )
        )
        row_actions = (
            create_edit_action(
                type_name="FloatingIpPriceEdit",
                name="update_floating_ip_price",
                verbose_name=_("Edit Floating IP Price"),
                url="horizon:admin:price_configuration:floating_ip_price_update"
            ),
            create_delete_action(
                type_name="FloatingIpPriceDelete",
                use_case=FloatingIpPriceUseCase(),
                single_action_label="Floating IP Price",
                plural_action_label="Floating IP Prices"
            )
        )


class RouterPriceTable(BasePriceTable):
    def get_object_display(self, datum):
        return datum['id']

    class Meta(object):
        name = "router_price"
        verbose_name = _("Router Price")
        table_actions = (
            create_filter_action(
                type_name="RouterPriceFilter",
                name="router_price_filter"
            ),
            create_create_action(
                type_name="RouterPriceCreate",
                name="create_router_price",
                verbose_name=_("Create Router Price"),
                url="horizon:admin:price_configuration:router_price_create",
                single_data=True,
            )
        )
        row_actions = (
            create_edit_action(
                type_name="RouterPriceEdit",
                name="update_router_price",
                verbose_name=_("Edit Router Price"),
                url="horizon:admin:price_configuration:router_price_update"
            ),
            create_delete_action(
                type_name="RouterPriceDelete",
                use_case=RouterPriceUseCase(),
                single_action_label="Router Price",
                plural_action_label="Router Prices"
            )
        )


class SnapshotPriceTable(BasePriceTable):
    def get_object_display(self, datum):
        return datum['id']

    class Meta(object):
        name = "snapshot_price"
        verbose_name = _("Snapshot Price")
        table_actions = (
            create_filter_action(
                type_name="SnapshotFilter",
                name="snapshot_price_filter"
            ),
            create_create_action(
                type_name="SnapshotCreate",
                name="create_snapshot_price",
                verbose_name=_("Create Snapshot Price"),
                url="horizon:admin:price_configuration:snapshot_price_create",
                single_data=True,
            )
        )
        row_actions = (
            create_edit_action(
                type_name="SnapshotEdit",
                name="update_snapshot_price",
                verbose_name=_("Edit Snapshot Price"),
                url="horizon:admin:price_configuration:snapshot_price_update"
            ),
            create_delete_action(
                type_name="SnapshotDelete",
                use_case=SnapshotPriceUseCase(),
                single_action_label="Snapshot Price",
                plural_action_label="Snapshot Prices"
            )
        )


class ImagePriceTable(BasePriceTable):
    def get_object_display(self, datum):
        return datum['id']

    class Meta(object):
        name = "image_price"
        verbose_name = _("Image Price")
        table_actions = (
            create_filter_action(
                type_name="ImageFilter",
                name="image_price_filter"
            ),
            create_create_action(
                type_name="ImageCreate",
                name="create_image_price",
                verbose_name=_("Create Image Price"),
                url="horizon:admin:price_configuration:image_price_create",
                single_data=True,
            )
        )
        row_actions = (
            create_edit_action(
                type_name="ImageEdit",
                name="update_image_price",
                verbose_name=_("Edit Image Price"),
                url="horizon:admin:price_configuration:image_price_update"
            ),
            create_delete_action(
                type_name="ImageDelete",
                use_case=ImagePriceUseCase(),
                single_action_label="Image Price",
                plural_action_label="Image Prices"
            )
        )
