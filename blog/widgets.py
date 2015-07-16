from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from ckeditor.widgets import CKEditorWidget

class MELeadMediaWidget(forms.Widget):
    template_name = 'admin/lead_media_field.html'

    class Media:
        js = (
            'http://code.jquery.com/jquery-1.11.2.min.js',
            'js/media_explorer/media_explorer.js',
            'js/lead_media_field_admin.js',
        )
        css = {
            'all': (
                'css/hide_media_fields.css',
            )
        }

    def render(self, name, value, attrs=None):
        context = { }
        return mark_safe(render_to_string(self.template_name, context))


class MECKEditorWidget(CKEditorWidget):

    class Media:
        js = (
            'http://code.jquery.com/jquery-1.11.2.min.js',
            'js/vendor/jQuery-Impromptu-6.1.0/jquery-impromptu.min.js',
            'js/media_explorer/media_explorer.js',
            'ckeditor/ckeditor/plugins/media_explorer/callback.js',
        )
        css = {
            'all': (
                'js/vendor/jQuery-Impromptu-6.1.0/jquery-impromptu.min.css',
            )
        }

