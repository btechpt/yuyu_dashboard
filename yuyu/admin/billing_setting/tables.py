from openstack_dashboard.dashboards.yuyu.core.billing_setting.tables import BaseUpdateSettingAction, BaseSettingTable


class UpdateSettingAction(BaseUpdateSettingAction):
    url = "horizon:admin:billing_setting:update_setting"


class SettingTable(BaseSettingTable):
    class Meta(object):
        table_actions = (UpdateSettingAction,)

