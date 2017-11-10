# -*- coding: utf-8 -*-

import time
import json

from django.http import HttpResponse

from django.conf import settings

from library import database as db
from library import tools

#=============================================================================

CREATE_STUDENT_ROLES = ["ta", "admin"]
CREATE_TA_ROLES = ["admin"]

def createStudent(request):
    try:
        if(request.session["user"]["role"] in  CREATE_STUDENT_ROLES):
            return createAccount(request, "student")
        else:
            return HttpResponse("Lack Permissions")

    except Exception as e:
        return HttpResponse(e)

def createTA(request):
    try:
        if(request.session["user"]["role"] in  CREATE_TA_ROLES):
            return createAccount(request, "ta")
        else:
            return HttpResponse("Lack Permissions")

    except Exception as e:
        return HttpResponse("You are not logged in")



def createAccount(request, role):
    
    # create assignment if user has permissions
    inputs = {"errors":"", "raw":request.POST}
    hasEmail = False
    hasPasswd = False

    try:
        inputs["name"] = request.POST["name"]
    except Exception as e:
        inputs["name"] = ""

    try:
        inputs["email"] = request.POST["email"]
        hasEmail = True
    except Exception as e:
        inputs["email"] = "ERROR NOT FOUND"

    try:
        inputs["password"] = request.POST["password"]
        hasPasswd = True
    except Exception as e:
        inputs["password"] = "ERROR NOT FOUND"

    try:
        if(hasEmail and hasPasswd):
            db.Query("INSERT INTO `user` (`name`, `email`, `password`, `role`, `enabled`) VALUES (%s, %s, md5(%s), %s, %s)", (inputs["name"], inputs["email"], inputs["password"], role, "yes"))
    except Exception as e:
        inputs["errors"] = e

    return HttpResponse("""<html lang="en">
<head>
<meta http-equiv="refresh" content="0; url=/html/Student%20Account%20Creation.html"/>
</head>
<body>{}</body>
</html>""".format(json.dumps(inputs)))


