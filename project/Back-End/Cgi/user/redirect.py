# -*- coding: utf-8 -*-

import time
import json

from django.http import QueryDict
from django.http import HttpResponse

from django.conf import settings

from library import database as db
from library import tools

#==============================================================================

ROOT = "/home/nginx/www/html/"

def getSingleAssignment(request, assignment):
    try:
        if(request.session["user"]):
            f = open(ROOT + "questionlist.html", 'r')
            return HttpResponse(f.read().format(assignment))
    except Exception as e:
        return HttpResponse(e) 
def createQuestionPage(request, assignment):
    try:
        if(request.session["user"]):
            f = open(ROOT + "questioncreation.html", 'r')
            return HttpResponse(f.read().format(assignment))
    except Exception as e:
        return HttpResponse(e)

def editQuestionPage(request, assignment, questions):
    try:
        if(request.session["user"]):
            f = open(ROOT + "questionedit.html", 'r')
            return HttpResponse(f.read().format(assignment, questions))
    except Exception as e:
        return HttpResponse(e)

