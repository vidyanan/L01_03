# -*- coding: utf-8 -*-

import json

from django.http import QueryDict
from django.http import HttpResponse

from django.conf import settings

from library import database as db
from library import tools

#==============================================================================

def getAssignments(request):
    try:
        if(request.session["user"]):
            # return template based on user
            assignments = {"a1":{"id":1, "name":"a1", "start-date":"2016-06-13", "end-date":"2019-03-11"}, "a2":{"id":2, "name":"a2", "start-date":"2011-01-14", "end-date":"2013-04-20"}, "errors":""}
            return HttpResponse(json.dumps(assignments), content_type="application/json")

    except Exception as e:
        return HttpResponse("Not logged in") 

def createAssignment(request):
    try:
        if(request.session["user"]):
            # create assignment if user has permissions
            inputs = {"errors":""}
            try:
                inputs["name"] = request.POST["name"]
            except Exception as e:
                inputs["name"] = "ERROR COULD NOT FIND"

            try:
                inputs["start-date"] = request.POST["start-date"]
            except Exception as e:
                inputs["start-date"] = "ERROR COULD NOT FIND"

            try:
                inputs["end-date"] = request.POST["end-date"]
            except Exception as e:
                inputs["end-date"] = "ERROR COULD NOT FIND"

            return HttpResponse(json.dumps(inputs), content_type="application/json")

    except Exception as e:
        
        return HttpResponse(str(e))
