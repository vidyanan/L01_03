# -*- coding: utf-8 -*-
import time

from django.http import QueryDict
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from library import database as db
from library import tools

#======================================================================
def me(request):
    try:
        return HttpResponse(str(request.session["user"]))
    except Exception as e:
        return HttpResponse("Not logged in")
