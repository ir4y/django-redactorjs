from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.conf import settings


GLOBAL_OPTIONS = getattr(settings, 'REDACTOR_OPTIONS', {'lang': 'en'})

INIT_JS = """<script type="text/javascript">
  jQuery(document).ready(function(){
    $("#%s").redactor(%s);
  });
</script>
"""


class RedactorEditor(widgets.Textarea):

    class Media:
        js = (
            'redactor/jquery-1.9.1.min.js',
            'redactor/redactor.min.js',
            'redactor/langs/{0}.js'.format(GLOBAL_OPTIONS['lang']),
        )
        css = {
            'all': (
                'redactor/css/redactor.css',
                'redactor/css/django_admin.css',
            )
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.custom_options = kwargs.pop('redactor_options', {})
        super(RedactorEditor, self).__init__(*args, **kwargs)

    def get_options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        options.update({
            'imageUpload': reverse('redactor_upload_image'),
            'imageGetJson': reverse('redactor_getjson_image'),
        })
        return json.dumps(options)

    def render(self, name, value, attrs=None):
        html = super(RedactorEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        html += INIT_JS % (id_, self.get_options())
        return mark_safe(html)


# For backward compatibility
JQueryEditor = RedactorEditor
