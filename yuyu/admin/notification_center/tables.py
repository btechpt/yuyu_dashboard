from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class NotificationFilterAction(tables.FilterAction):
    name = "notification_center_filter"


class NotificationTable(tables.DataTable):
    title = tables.WrappingColumn("title", verbose_name=_("Title"),
                                  link="horizon:admin:notification_center:detail")
    short_description = tables.Column("short_description", verbose_name=_("Short Description"))
    recipient = tables.Column("recipient", verbose_name=_("Recipient"))
    sent_status = tables.Column("sent_status", verbose_name=_("Sent Status"))
    is_read = tables.Column("is_read", verbose_name=_("Is Read"))
    created_at = tables.Column("created_at", verbose_name=_("Created At"))

    def get_object_id(self, obj):
        return obj["id"]

    class Meta(object):
        name = "list_notification_center"
        verbose_name = _("Notification Center")
        multi_select = False
        table_actions = (NotificationFilterAction, )
