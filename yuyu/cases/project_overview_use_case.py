from openstack_dashboard.dashboards.yuyu.core import yuyu_client


class ProjectOverviewUseCase:
    def get_tenant(self, request):
        response = yuyu_client.get(request, f"project_overview/{request.user.tenant_id}/get_tenant/")
        keys_to_include = ['email_notification', ]

        return [x for x in response.json().items() if x[0] in keys_to_include]

    def update_email(self, request, payload):
        return yuyu_client.post(request, f"project_overview/{request.user.tenant_id}/update_email/", payload).json()

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
