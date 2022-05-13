from openstack_dashboard.dashboards.yuyu.core import yuyu_client


class SettingUseCase:
    def get_settings(self, request):
        return yuyu_client.get(request, "settings/").json()

    def set_setting(self, request, key, value):
        return yuyu_client.patch(request, f"settings/{key}/", {
            "value": value
        }).json()
