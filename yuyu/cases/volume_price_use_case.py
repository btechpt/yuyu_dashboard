from openstack_dashboard import api
from openstack_dashboard.dashboards.yuyu.cases.pricing_use_case import PricingUseCase


class VolumePriceUseCase(PricingUseCase):
    pricing_name = "volume"

    def list(self, request):
        data = list(super().list(request))

        for d in data:
            d["name"] = api.cinder.volume_type_get(request, d['volume_type_id']).name

        return data

    def get(self, request, id):
        data = super().get(request, id)
        data["name"] = api.cinder.volume_type_get(request, data['volume_type_id']).name
        return data

    def has_missing_price(self, request):
        server_data_prices = list(map(lambda d: d['volume_type_id'], super().list(request)))
        volume_types = api.cinder.volume_type_list(request)

        for f in volume_types:
            if f.id not in server_data_prices:
                return True

        return False
