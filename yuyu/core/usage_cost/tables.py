from django.utils.translation import ugettext_lazy as _

from horizon import tables


class InstanceCostTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Name'))
    flavor = tables.Column('flavor', verbose_name=_('Flavor'))
    usage = tables.Column('usage', verbose_name=_('Usage'))
    cost = tables.Column('cost', verbose_name=_('Cost'))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "instance_cost"
        hidden_title = False
        verbose_name = _("Instance")


class VolumeCostTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Name'))
    type = tables.Column('type', verbose_name=_('Type'))
    size = tables.Column('size', verbose_name=_('Size'))
    usage = tables.Column('usage', verbose_name=_('Usage'))
    cost = tables.Column('cost', verbose_name=_('Cost'))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "volume_cost"
        hidden_title = False
        verbose_name = _("Volume")


class FloatingIpCostTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Name'))
    usage = tables.Column('usage', verbose_name=_('Usage'))
    cost = tables.Column('cost', verbose_name=_('Cost'))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "floating_ip_cost"
        hidden_title = False
        verbose_name = _("Floating IP")


class RouterCostTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Name'))
    usage = tables.Column('usage', verbose_name=_('Usage'))
    cost = tables.Column('cost', verbose_name=_('Cost'))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "router_cost"
        hidden_title = False
        verbose_name = _("Router")


class SnapshotCostTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Name'))
    size = tables.Column('size', verbose_name=_('Size'))
    usage = tables.Column('usage', verbose_name=_('Usage'))
    cost = tables.Column('cost', verbose_name=_('Cost'))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "snapshot_cost"
        hidden_title = False
        verbose_name = _("Snapshot")


class ImageCostTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Name'))
    size = tables.Column('size', verbose_name=_('Size'))
    usage = tables.Column('usage', verbose_name=_('Usage'))
    cost = tables.Column('cost', verbose_name=_('Cost'))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta(object):
        name = "image_cost"
        hidden_title = False
        verbose_name = _("Image")
