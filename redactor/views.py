import json
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from settings import IS_REDACTOR_PUBLIC
from models import RedaktorJsFile

try:
    from sorl.thumbnail import get_thumbnail
except ImportError:
    get_thumbnail = None


@csrf_exempt
@require_POST
@login_required
def redactor_upload(request):
    images = []
    for f in request.FILES.getlist("file"):
        obj = RedaktorJsFile.objects.create(upload=f, is_image=True, owner=request.user)
        images.append({"filelink": obj.upload.url})
    return HttpResponse(json.dumps(images), mimetype="application/json")


@login_required
def redactor_recent_json(request):
    def get_thumbnail_url(image):
        if get_thumbnail:
            return get_thumbnail(image.path, '64x64', crop='center', quality=99).url
        return image.url

    query = Q(is_image=True)
    if not IS_REDACTOR_PUBLIC:
        query &= Q(owner=request.user)

    images = [
        {"thumb": get_thumbnail_url(obj.upload), "image": obj.upload.url}
        for obj in RedaktorJsFile.objects.filter(query).order_by("-date_created")[:20]
    ]
    return HttpResponse(json.dumps(images), mimetype="application/json")