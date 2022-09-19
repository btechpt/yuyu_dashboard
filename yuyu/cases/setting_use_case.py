from openstack_dashboard.dashboards.yuyu.core import yuyu_client

from django.utils.html import format_html


class SettingUseCase:

    def get_settings(self, request, transform_logo=True):
        response = yuyu_client.get(request, "settings/").json()

        if transform_logo and response["company_logo"]:
            # convert base64 img
            response['company_logo'] = format_html(
                '<img height="50" src="data:;base64,{}">',
                response['company_logo']
            )

        return response

    def set_setting(self, request, key, value):
        return yuyu_client.patch(request, f"settings/{key}/", {
            "value": value
        }).json()

    def get_setting_admin(self, request, transform_logo=True):
        keys_to_exclude = ['billing_enabled']
        response = self.get_settings(request, transform_logo=transform_logo)

        return [x for x in response.items() if x[0] not in keys_to_exclude]

    def has_missing_setting(self, request):
        missing = [None, '']
        response = self.get_settings(request)
        context = {x[0]: True for x in response.items() if x[1] in missing}

        if context:
            context['has_missing'] = True
            return context

        context['has_missing'] = False

        return context
