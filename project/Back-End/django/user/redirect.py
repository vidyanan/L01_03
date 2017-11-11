# -*- coding: utf-8 -*-

import time
import json

from django.http import QueryDict
from django.http import HttpResponse

from django.conf import settings

from library import database as db
from library import tools

#==============================================================================

ROOT = "/home/nginx/www/html"

def getSingleAssignment(request, assignment):
    try:
        if(request.session["user"]):
            f = open(ROOT + "", 'w')
            return HttpResponse(f.read().format(assignment))
    except Exception as e:
        return HttpResponse(e) 

