import json

from django.conf.urls.defaults import url, patterns

from redactor.views import redactor_upload,redactor_json
from redactor.forms import FileForm, ImageForm


urlpatterns = patterns('',
    url('^upload/image/(?P<upload_to>.*)', redactor_upload, {
        'form_class': ImageForm,
        'response': lambda name, url: '<img src="%s" alt="%s" />' % (url, name),
    }, name='redactor_upload_image'),

    url('^upload/file/(?P<upload_to>.*)', redactor_upload, {
        'form_class': FileForm,
        'response': lambda name, url: json.dumps({'filelink':url,'filename':name}),
        }, name='redactor_upload_file'),

    url('^json/image/(?P<upload_to>.*)', redactor_json, name='redactor_getjson_image'),
)
