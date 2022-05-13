from openstack_dashboard import api
from openstack_dashboard.dashboards.yuyu.cases.pricing_use_case import PricingUseCase


class FlavorPriceUseCase(PricingUseCase):
    pricing_name = "flavor"

    def list(self, request):
        data = list(super().list(request))

        for d in data:
            try:
                flavor = api.nova.flavor_get(request, d['flavor_id'])
                d["name"] = flavor.name
            except Exception:
                d["name"] = 'Invalid Flavor'

        return data

    def get(self, request, id):
        data = super().get(request, id)
        try:
            flavor = api.nova.flavor_get(request, d['flavor_id'])
            data["name"] = flavor.name
        except Exception:
            data["name"] = 'Invalid Flavor'

        return data

    def has_missing_price(self, request):
        server_data_prices = list(map(lambda d: d['flavor_id'], super().list(request)))
        flavor_list = api.nova.flavor_list(request)

        for f in flavor_list:
            if f.id not in server_data_prices:
                return True

        return False