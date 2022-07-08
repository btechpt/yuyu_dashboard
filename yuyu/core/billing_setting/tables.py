from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class SettingName:
    SETTING_NAMES = {
        "billing_enabled": _("Billing Enabled"),
        "invoice_tax": _("Invoice Tax"),
        "company_name": _("Company Name"),
        "company_logo": _("Company Logo"),
        "company_address": _("Company Address"),
        "email_admin": _("Email Admin"),
        "email_notification": _("Email Notification")
    }

    def get_setting_name(self, setting):
        return self.SETTING_NAMES.get(setting[0], setting[0].replace("_", " ").title())

    def get_setting_value(self, setting):
        return setting[1]


class BaseUpdateSettingAction(tables.LinkAction):
    name = "update_setting"
    verbose_name = _("Update Setting")
    url = None
    classes = ("ajax-modal",)
    icon = "pencil"
    step = None

    def get_link_url(self, datum=None):
        return reverse(self.url)


class BaseSettingTable(tables.DataTable):
    setting_name = SettingName()
    name = tables.Column(setting_name.get_setting_name, verbose_name=_('Setting Name'))
    value = tables.Column(setting_name.get_setting_value, verbose_name=_('Value'))

    def get_object_id(self, obj):
        return obj

    class Meta(object):
        name = "settings"
        verbose_name = _("Settings")
        multi_select = False
