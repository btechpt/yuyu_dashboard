from django.utils.translation import ugettext_lazy as _
from djmoney.forms import MoneyField

from openstack_dashboard.dashboards.yuyu.cases.pricing_use_case import PricingUseCase
from horizon import exceptions
from horizon import forms
from horizon import messages


class BasePriceForm(forms.SelfHandlingForm):
    hourly_price = MoneyField(label=_("Hourly Price"), min_value=0, max_digits=10)
    monthly_price = MoneyField(label=_("Monthly Price"), min_value=0, max_digits=10, required=False)

    USE_CASE: PricingUseCase = None
    NAME = ""

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.model_id = kwargs.get('initial', {}).get('model_id', None)

    def to_payload(self, data):
        payload = {
            "hourly_price": data['hourly_price'].amount,
            "hourly_price_currency": data['hourly_price'].currency.code
        }

        if data['monthly_price']:
            payload['monthly_price'] = data['monthly_price'].amount
            payload['monthly_price_currency'] = data['monthly_price'].currency.code

        return payload

    def handle(self, request, data):
        try:
            if self.model_id:
                result = self.USE_CASE.update(
                    request=request,
                    id=self.model_id,
                    payload=self.to_payload(data)
                )
                messages.success(request, _(f"Successfully update {self.NAME}"))
            else:
                result = self.USE_CASE.create(
                    request=request,
                    payload=self.to_payload(data)
                )
                messages.success(request, _(f"Successfully create {self.NAME}"))

            return result
        except Exception:
            mode_str = "update" if self.model_id else "create"
            exceptions.handle(request, _(f'Unable to {mode_str} {self.NAME}.'))
