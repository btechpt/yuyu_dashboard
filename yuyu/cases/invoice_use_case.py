import dateutil.parser
import requests
from djmoney.money import Money
from openstack_dashboard import api
from openstack_dashboard.dashboards.yuyu.core import yuyu_client
from openstack_dashboard.dashboards.yuyu.core.utils.invoice_utils import state_to_text


class InvoiceUseCase:
    def get_simple_list(self, request, tenant_id=None):
        if not tenant_id:
            tenant_id = request.user.project_id
        response = yuyu_client.get(request, f"invoice/simple_list/?tenant_id={tenant_id}")
        data = response.json()

        for d in data:
            zero_money = Money(amount=0, currency=d['subtotal_currency'])
            d['start_date'] = dateutil.parser.isoparse(d['start_date'])
            d['subtotal_money'] = Money(amount=d['subtotal'], currency=d['subtotal_currency'])
            d['total_money'] = Money(amount=d['total'], currency=d['total_currency']) if d['total'] else zero_money
            d['state_text'] = state_to_text(d['state'])
        return data

    def get_invoice(self, request, id, tenant_id=None):
        if not tenant_id:
            tenant_id = request.user.project_id

        response = yuyu_client.get(request, f"invoice/{id}/?tenant_id={tenant_id}")
        data = response.json()
        data['subtotal_money'] = Money(amount=data['subtotal'], currency=data['subtotal_currency'])

        zero_money = Money(amount=0, currency=data['subtotal_currency'])

        data['tax_money'] = Money(amount=data['tax'], currency=data['tax_currency']) if data['tax'] else zero_money
        data['total_money'] = Money(amount=data['total'], currency=data['total_currency']) if data[
            'total'] else zero_money

        data['start_date'] = dateutil.parser.isoparse(data['start_date'])
        data['state_text'] = state_to_text(data['state'])

        return data

    def enable_billing(self, request):
        volume_type_list = api.cinder.volume_type_list(request)
        volume_type_name_to_id = {
            v.name: v.id
            for v in volume_type_list
        }

        router_with_ext = filter(lambda r: bool(r.external_gateway_info), api.neutron.router_list(request))
        instances = api.nova.server_list(request, search_opts={'all_tenants': True})[0]
        volumes = api.cinder.volume_list(request, search_opts={"all_tenants": 1})
        floating_ips = api.neutron.tenant_floating_ip_list(request, all_tenants=True)
        snapshots = api.cinder.volume_snapshot_list(request, search_opts={'all_tenants': True})
        images = api.glance.image_list_detailed(request, filters={'is_public': None})[0]

        # Note!: When initializing router, we don't know when external network was added to router
        payload = {
            "instances": list(map(lambda s: {
                "tenant_id": s.tenant_id,
                "instance_id": s.id,
                "name": s.name,
                "flavor_id": s.flavor['id'],
                "start_date": s.created
            }, instances)),
            "volumes": list(map(lambda v: {
                "tenant_id": v.tenant_id,
                "volume_id": v.id,
                "volume_name": v.name,
                "volume_type_id": volume_type_name_to_id[v.volume_type],
                "space_allocation_gb": v.size,
                "start_date": v.created_at
            }, volumes)),
            "floating_ips": list(map(lambda f: {
                "tenant_id": f.tenant_id,
                "fip_id": f.id,
                "ip": f.ip,
                "start_date": f.created_at
            }, floating_ips)),
            "routers": list(map(lambda r: {
                "tenant_id": r.tenant_id,
                "router_id": r.id,
                "name": r.name,
                "start_date": r.created_at
            }, router_with_ext)),
            "snapshots": list(map(lambda s: {
                "tenant_id": s.project_id,
                "snapshot_id": s.id,
                "name": s.name,
                "space_allocation_gb": s.size,
                "start_date": s.created_at
            }, snapshots)),
            "images": list(map(lambda i: {
                "tenant_id": i.owner,
                "image_id": i.id,
                "name": i.name,
                "space_allocation_gb": i.size / 1024 / 1024 / 1024,
                "start_date": i.created_at
            }, images))
        }

        response = yuyu_client.post(request, f"invoice/enable_billing/", payload)
        if response.status_code == 200:
            return True
        raise Exception('Unable to enable billing')

    def disable_billing(self, request):
        yuyu_client.post(request, f"invoice/disable_billing/", {})

    def reset_billing(self, request):
        yuyu_client.post(request, f"invoice/reset_billing/", {})

    def finish_invoice(self, request, id):
        response = yuyu_client.get(request, f"invoice/{id}/finish/")
        data = response.json()
        return data

    def rollback_to_unpaid_invoice(self, request, id):
        response = yuyu_client.get(request, f"invoice/{id}/rollback_to_unpaid/")
        data = response.json()
        return data