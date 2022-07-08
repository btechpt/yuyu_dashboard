from django.utils.translation import ugettext_lazy as _

from horizon import forms, messages, exceptions
from openstack_dashboard.dashboards.yuyu.cases.project_overview_use_case import ProjectOverviewUseCase


class SettingForm(forms.SelfHandlingForm):
    NAME = "Settings"
    USE_CASE = ProjectOverviewUseCase()

    email_notification = forms.EmailField(label=_("EMAIL NOTIFICATION"),
                                          required=True)

    def handle(self, request, data):
        try:
            print(data)
            result = self.USE_CASE.update_email(
                request=request,
                payload=data
            )
            messages.success(request, _(f"Successfully update {self.NAME}"))

            return result
        except Exception as e:
            exceptions.handle(request,
                              _('Unable to update.'))
