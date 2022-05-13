from openstack_dashboard.dashboards.yuyu.core import yuyu_client


class ProjectOverviewUseCase:
    def total_resource(self, request):
        response = yuyu_client.get(request, f"project_overview/total_resource/?tenant_id={request.user.tenant_id}")
        return response.json()

    def active_resource(self, request):
        response = yuyu_client.get(request, f"project_overview/active_resource/?tenant_id={request.user.tenant_id}")
        return response.json()

    def price_total_resource(self, request):
        response = yuyu_client.get(request, f"project_overview/price_total_resource/?tenant_id={request.user.tenant_id}")
        return response.json()

    def price_active_resource(self, request):
        response = yuyu_client.get(request, f"project_overview/price_active_resource/?tenant_id={request.user.tenant_id}")
        return response.json()
