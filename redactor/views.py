import os
import json
from os.path import join
import Image

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from redactor.forms import ImageForm


UPLOAD_PATH = getattr(settings, 'REDACTOR_UPLOAD', 'redactor/')


@csrf_exempt
@require_POST
@user_passes_test(lambda u: u.is_staff)
def redactor_upload(request, upload_to=None, form_class=ImageForm, response=lambda name, url: url):
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        file_ = form.cleaned_data['file']
        path = os.path.join(upload_to or UPLOAD_PATH, file_.name)
        real_path = default_storage.save(path, file_)
        return HttpResponse(
            response(file_.name, os.path.join(settings.MEDIA_URL, real_path))
        )
    return HttpResponse(status=403)

@user_passes_test(lambda u: u.is_staff)
def redactor_json(request,upload_to=None):
    if not upload_to:
        upload_to = settings.REDACTOR_UPLOAD
    images= []
    for root, subFolders, files in os.walk(join(settings.MEDIA_ROOT, upload_to)):
        for file in files:
            if file.endswith(u'.thumbnail.jpg'):
                continue
            try:
                image = u"{0}{1}{2}".format(settings.MEDIA_URL,upload_to,file)
                image_file = u"{0}/{1}{2}".format(settings.MEDIA_ROOT,upload_to,file)
                thumb = u"{0}{1}{2}.thumbnail.jpg".format(settings.MEDIA_URL,upload_to,file)
                thumb_file = u"{0}/{1}{2}.thumbnail.jpg".format(settings.MEDIA_ROOT,upload_to,file)
                if not os.path.exists(thumb):
                    im = Image.open(image_file)
                    im.thumbnail((100,74,), Image.ANTIALIAS)
                    im.save(thumb_file, "JPEG")
                images.append({'thumb':thumb,'image':image})
                print(files)
            except IOError:
                continue
    return HttpResponse(json.dumps(images),mimetype="application/json")