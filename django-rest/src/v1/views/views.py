import re

from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.apps import apps
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.utils.cache import get_cache_key
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


@cache_page(60 * 60)
@api_view(["GET"])
@permission_classes((AllowAny,))
def welcome(request):
    f = open("CHANGELOG.md", "r")
    data = f.read()
    version = re.findall("v[0-9]+\.[0-9]+\.[0-9]+", data)[0]
    f.close()

    return JsonResponse(
        {"message": f"welcome customer service APIs!", "api_version": version}, status=status.HTTP_200_OK
    )
