import base64

from django.utils.translation import ugettext_lazy as _

from horizon import forms, messages, exceptions
from openstack_dashboard.dashboards.yuyu.cases.setting_use_case import SettingUseCase


class SettingForm(forms.SelfHandlingForm):
    NAME = "Settings"
    USE_CASE = SettingUseCase()

    company_name = forms.CharField(label=_("COMPANY NAME"),
                                   required=False)

    company_logo = forms.ImageField(label=_("COMPANY LOGO"),
                                    required=False)
    company_address = forms.CharField(label=_("COMPANY ADDRESS"),
                                      required=False, widget=forms.Textarea())
    email_admin = forms.EmailField(label=_("EMAIL ADMIN"),
                                   required=True)

    invoice_tax = forms.IntegerField(label=_("INVOICE TAX (%)"),
                                     required=True)

    def clean(self):
        data = super(SettingForm, self).clean()
        company_logo = data.get('company_logo', None)

        if company_logo:
            company_logo = self.files['company_logo'].read()
            encoded_string = base64.b64encode(company_logo)
            data["company_logo"] = encoded_string

        return data

    def handle(self, request, data):
        try:
            result = ""
            for k, v in data.items():
                if k == 'company_logo' and v is None:
                    continue

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
