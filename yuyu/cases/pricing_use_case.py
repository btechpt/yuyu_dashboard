from django.conf import settings
from djmoney.money import Money

from openstack_dashboard.dashboards.yuyu.core import yuyu_client


class PricingUseCase:
    pricing_name = ""

    def clean_price_response(self, response_data):
        response_data["hourly_price"] = Money(amount=response_data['hourly_price'],
                                              currency=response_data['hourly_price_currency'])
        if response_data['monthly_price'] and response_data['monthly_price_currency']:
            response_data["monthly_price"] = Money(amount=response_data['monthly_price'],
                                                   currency=response_data['monthly_price_currency'])
        else:
            response_data["monthly_price"] = Money(currency=settings.DEFAULT_CURRENCY)

        return response_data

    def create(self, request, payload):
        return yuyu_client.post(request, f"price/{self.pricing_name}/", payload).json()

    def update(self, request, id, payload):
        return yuyu_client.patch(request, f"price/{self.pricing_name}/{id}/", payload).json()

    def delete(self, request, id):
        return yuyu_client.delete(request, f"price/{self.pricing_name}/{id}/")

    def list(self, request):
        response = yuyu_client.get(request, f"price/{self.pricing_name}/")
        data = list(map(lambda f: self.clean_price_response(f), response.json()))
        return data

    def get(self, request, id):
        data = yuyu_client.get(request, f"price/{self.pricing_name}/{id}/").json()
        data = self.clean_price_response(data)
        return data

    def has_missing_price(self, request):
        return len(self.list(request)) == 0