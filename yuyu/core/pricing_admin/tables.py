from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

from horizon import tables, exceptions


class BaseCreatePrice(tables.LinkAction):
    classes = ("ajax-modal",)
    icon = "link"
    single_data = False

    def allowed(self, request, datum):
        if self.single_data and len(self.table.data) >= 1:
            self.classes = [c for c in self.classes] + ['hidden']

        return True


class BaseEditPrice(tables.LinkAction):
    classes = ("ajax-modal",)
    icon = "pencil"

    def get_link_url(self, datum=None):
        instance_id = self.table.get_object_id(datum)
        return reverse(self.url, args=[instance_id])


class BaseDeletePrice(tables.DeleteAction):
    use_case = None
    single_action_label = None
    plural_action_label = None

    def action_present(self, count):
        return ungettext_lazy(
            "Delete " + self.single_action_label,
            "Delete " + self.plural_action_label,
            count
        )

    def action_past(self, count):
        return ungettext_lazy(
            "Deleted " + self.single_action_label,
            "Deleted " + self.plural_action_label,
            count
        )

    def delete(self, request, obj_id):
        try:
            self.use_case.delete(request, obj_id)
        except Exception as e:
            print("Exception", e)
            exceptions.handle(request, e)


class BasePriceTable(tables.DataTable):
    hourly_price = tables.Column('hourly_price', verbose_name=_('Hourly Price'))
    monthly_price = tables.Column('monthly_price', verbose_name=_('Monthly Price'))

    def get_object_id(self, datum):
        return datum['id']
