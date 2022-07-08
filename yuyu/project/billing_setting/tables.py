from openstack_dashboard.dashboards.yuyu.core.billing_setting.tables import BaseSettingTable, BaseUpdateSettingAction


class UpdateSettingAction(BaseUpdateSettingAction):
    url = "horizon:project:billing_setting:update_setting"


class SettingTable(BaseSettingTable):
    class Meta(object):
        table_actions = (UpdateSettingAction,)
