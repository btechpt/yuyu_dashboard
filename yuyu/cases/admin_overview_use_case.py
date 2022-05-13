from openstack_dashboard.dashboards.yuyu.core import yuyu_client


class AdminOverviewUseCase:
    def total_resource(self, request):
        response = yuyu_client.get(request, f"admin_overview/total_resource/")
        return response.json()

    def active_resource(self, request):
        response = yuyu_client.get(request, f"admin_overview/active_resource/")
        return response.json()

    def price_total_resource(self, request):
        response = yuyu_client.get(request, f"admin_overview/price_total_resource/")
        return response.json()

    def price_active_resource(self, request):
        response = yuyu_client.get(request, f"admin_overview/price_active_resource/")
        return response.json()
