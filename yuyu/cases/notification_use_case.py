from openstack_dashboard.dashboards.yuyu.core import yuyu_client


class NotificationCenterUseCase:
    def get_list(self, request, filter_selection=None):
        if filter_selection is None:
            return yuyu_client.get(request, f"notification/").json()

        return yuyu_client.get(request, f"notification/?tenant_id={filter_selection}").json()

    def get_detail(self, request, notification_id):
        response = yuyu_client.get(request, f"notification/{notification_id}").json()
        return response

    def set_read(self, request, notification_id=None):
        return yuyu_client.get(request, f"notification/{notification_id}/set_read/").json()

    def set_resend(self, request, notification_id):
        return yuyu_client.get(request, f"notification/{notification_id}/resend/").json()

