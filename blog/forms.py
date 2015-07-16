from django import forms
from blog.models import Blog
from blog.widgets import MELeadMediaWidget
from blog.widgets import MECKEditorWidget

class BlogAdminForm(forms.ModelForm):
    lead_media_widget = forms.CharField(required=False,label="Lead Media",widget=MELeadMediaWidget())

    class Meta:
        model = Blog
        widgets = {
            'content': MECKEditorWidget,
            'lead_media_type': forms.HiddenInput(),
            'lead_media_id': forms.HiddenInput(),
            'lead_media_caption': forms.HiddenInput(),
            'lead_media_credit': forms.HiddenInput(),
        }

