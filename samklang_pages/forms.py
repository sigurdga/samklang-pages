from django.forms import ModelForm, RegexField, ModelChoiceField
from django.contrib.auth.models import Group
from samklang_pages.models import Page
from django.utils.translation import ugettext_lazy as _

class PageForm(ModelForm):
    url = RegexField(
            label=_("URL"),
            max_length=100,
            regex=r'^[-\w/]+$',
            help_text = _("Example: '/about/contact/'. Make sure to have leading"
                " and trailing slashes."),
            error_message = _("This value must contain only letters, numbers,"
                " underscores, dashes or slashes."),
            )
    group = ModelChoiceField(Group.objects, empty_label=_("Public"), required=False, label=_("Read permission"))

    class Meta:
        model = Page
        exclude = ('content_html', 'user', 'site')
