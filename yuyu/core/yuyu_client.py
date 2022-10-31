import requests
from django.conf import settings


def _get_header(request):
    return {}


def _yuyu_url(request, path):
    yuyu_url = settings.YUYU_URL
    if hasattr(settings, 'YUYU_URL_REGION'):
        regions = dict(settings.YUYU_URL_REGION)
        region_url = regions.get(request.session['region_name'])
        if region_url:
            yuyu_url = region_url

    return yuyu_url + "/api/" + path


def get(request, path):
    return requests.get(_yuyu_url(request, path), headers=_get_header(request))


def post(request, path, payload):
    return requests.post(_yuyu_url(request, path), headers=_get_header(request), json=payload)


def patch(request, path, payload):
    return requests.patch(_yuyu_url(request, path), headers=_get_header(request), json=payload)


def delete(request, path):
    return requests.delete(_yuyu_url(request, path), headers=_get_header(request))
