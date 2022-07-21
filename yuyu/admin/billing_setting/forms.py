from django.utils.translation import ugettext_lazy as _

from horizon import forms, messages, exceptions
from openstack_dashboard.dashboards.yuyu.cases.setting_use_case import SettingUseCase


class SettingForm(forms.SelfHandlingForm):
    NAME = "Settings"
    USE_CASE = SettingUseCase()

    company_name = forms.CharField(label=_("COMPANY NAME"),
                                   required=False)
    company_logo = forms.URLField(label=_("COMPANY LOGO URL"),
                                  required=False)
    company_address = forms.CharField(label=_("COMPANY ADDRESS"),
                                      required=False, widget=forms.Textarea())
    email_admin = forms.EmailField(label=_("EMAIL ADMIN"),
                                   required=True)

    invoice_tax = forms.IntegerField(label=_("INVOICE TAX (%)"),
                                     required=True)

    def handle(self, request, data):
        try:
            result = ""
            for k, v in data.items():
                result = self.USE_CASE.set_setting(
                    request=request,
                    key=k,
                    value=v
                )
            messages.success(request, _(f"Successfully update {self.NAME}"))

            return result
        except Exception as e:
            exceptions.handle(request,
                              _('Unable to update.'))
