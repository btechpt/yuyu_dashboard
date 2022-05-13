from openstack_dashboard.dashboards.yuyu.cases.flavor_price_use_case import FlavorPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.floating_ip_price_use_case import FloatingIpPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.image_price_use_case import ImagePriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.router_price_use_case import RouterPriceUseCase
from openstack_dashboard.dashboards.yuyu.cases.volume_price_use_case import VolumePriceUseCase


def has_missing_price(request):
    flavor_price_uc = FlavorPriceUseCase()
    volume_price_uc = VolumePriceUseCase()
    fip_price_uc = FloatingIpPriceUseCase()
    router_price_uc = RouterPriceUseCase()
    snapshot_price_uc = RouterPriceUseCase()
    image_price_uc = ImagePriceUseCase()

    context = {
        'flavor': flavor_price_uc.has_missing_price(request),
        'volume': volume_price_uc.has_missing_price(request),
        'fip': fip_price_uc.has_missing_price(request),
        'router': router_price_uc.has_missing_price(request),
        'snapshot': snapshot_price_uc.has_missing_price(request),
        'image': image_price_uc.has_missing_price(request),
    }

    context['has_missing'] = context['flavor'] or context['volume'] or context['fip'] or context['router'] or context[
        'snapshot'] or context['image']

    return context
