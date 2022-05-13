from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from openstack_dashboard.dashboards.yuyu.cases.pricing_use_case import PricingUseCase


class BasePriceIndexView(tables.DataTableView):
    USE_CASE: PricingUseCase = None

    def has_more_data(self, table):
        return self._has_more

    def get_data(self):
        try:
            datas = self.USE_CASE.list(self.request)
            self._has_more = False  # TODO: Pagination
            return datas
        except Exception:
            self._has_more = False
            error_message = _('Unable to get data')
            exceptions.handle(self.request, error_message)

            return []
