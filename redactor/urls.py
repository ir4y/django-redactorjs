import json

from django.conf.urls import url, patterns

from redactor.views import redactor_upload,redactor_recent_json


urlpatterns = patterns('',
    url('^upload/image/$', redactor_upload, name='redactor_upload_image'),
    url('^json/image/$', redactor_recent_json, name='redactor_getjson_image'),
)
