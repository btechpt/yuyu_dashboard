import requests
from django.conf import settings


def _get_header(request):
    return {}


def _yuyu_url(request, path):
    return settings.YUYU_URL + "/api/" + path


def get(request, path):
    return requests.get(_yuyu_url(request, path), headers=_get_header(request))


def post(request, path, payload):
    return requests.post(_yuyu_url(request, path), headers=_get_header(request), json=payload)


def patch(request, path, payload):
    return requests.patch(_yuyu_url(request, path), headers=_get_header(request), json=payload)


def delete(request, path):
    return requests.delete(_yuyu_url(request, path), headers=_get_header(request))
