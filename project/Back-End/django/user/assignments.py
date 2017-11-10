# -*- coding: utf-8 -*-

import time
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
            #return template based on user
            #result = {"errors":""}
            result = dict()
            arrayToAdd = []
            assignments = db.Query(
                """     SELECT *
                        FROM `assignments`
                                """,
                ())

            for assignment in assignments:
                temp = dict()
                temp["id"] = assignment["id"]
                temp["name"] = assignment["name"]
                temp["start-date"] = assignment["start-date"]
                temp["end-date"] = assignment["end-date"]
                arrayToAdd.append(temp)
            result["assignments"] = arrayToAdd
            return HttpResponse(json.dumps(result), content_type="application/json")

    except Exception as e:
        return HttpResponse(e) 

def createAssignment(request):
    try:
        if(request.session["user"]):
            # create assignment if user has permissions
            inputs = {"errors":"", "raw":request.POST}
            reqInputs = False

            try:
                inputs["name"] = request.POST["name"]
                reqInputs = True
            except Exception as e:
                inputs["name"] = "ERROR COULD NOT FIND"

            try:
                inputs["start-date"] = request.POST["start-date"]
            except Exception as e:
                inputs["start-date"] = ""

            try:
                inputs["end-date"] = request.POST["end-date"]
            except Exception as e:
                inputs["end-date"] = ""
            try:
                if(reqInputs):
                    db.Query("INSERT INTO `assignments` (`name`, `start-date`, `end-date`) VALUES (%s, %s, %s)", (inputs["name"], inputs["start-date"], inputs["end-date"]))
            except Exception as e:
                inputs["errors"] = e

            return HttpResponse("""<html lang="en">
<head>
<meta http-equiv="refresh" content="0; url=/html/assignmentlist.html"/>
</head>
<body>%s</body>
</html>""", (json.dumps(inputs)))

    except Exception as e:
        
        return HttpResponse(e)

def editAssignments(request, assignment):
    try:
        if(request.session["user"]):
            # edit an assignment if user has permissions
            inputs = {"errors":"", "raw":request.POST, "assignment":assignment}
            reqInputs = False

            try:
                inputs["name"] = request.POST["name"]
                reqInputs = True
            except Exception as e:
                inputs["name"] = "ERROR COULD NOT FIND"

            try:
                inputs["start-date"] = request.POST["start-date"]
            except Exception as e:
                inputs["start-date"] = ""

            try:
                inputs["end-date"] = request.POST["end-date"]
            except Exception as e:
                inputs["end-date"] = ""
            try:
                if(reqInputs):
                    db.Query("UPDATE assignments SET `name`=%s, `start-date`=%s, `end-date`=%s WHERE id=%s", (inputs["name"], inputs["start-date"], inputs["end-date"], inputs["assignment"]))
            except Exception as e:
                inputs["errors"] = e

            return HttpResponse(json.dumps(inputs), content_type="application/json")

    except Exception as e:

        return HttpResponse(e)

def getQuestions(request, assignment):
    try:
        if(request.session["user"]):
            result = {"errors":""}
            arrayToAdd = []
            questions=db.Query(
                """    SELECT *
                       FROM `questions`
                       WHERE `assignment`=%s""", (assignment))

            for question in questions:
                temp = dict()
                temp["id"] = question["id"]
                temp["name"] = question["name"]
                temp["type"] = question["type"]
                temp["question"] = question["question"]
                temp["answer"] = question["answer"]
                arrayToAdd.append(temp)

            result["questions"] = arrayToAdd

            return HttpResponse(json.dumps(result), content_type="application/json")

    except Exception as e:

        return HttpResponse(e)


def createQuestion(request, assignment):
    try:

        if(request.session["user"]):
            inputs = {"assignment":assignment, "errors":""}

            try:
                inputs["name"] = request.POST["name"]
            except Exception as e:
                inputs["name"] = ""

            try:
                inputs["type"] = request.POST["type"] 
            except Exception as e:
                inputs["type"] = ""

            try:
                inputs["question"] = request.POST["question"]
            except Exception as e:
                inputs["question"] = ""

            try:
                inputs["answer"] = request.POST["answer"]
            except Exception as e:
                inputs["answer"] = ""

            try:
                if(len(inputs["question"]) != 0 and len(inputs["answer"]) != 0 and len(inputs["type"]) != 0):
                    db.Query(
                    """     INSERT INTO `questions` (`name`, `type`, `questions`, `answer`, `assignment`)
                            VALUES (%s, %s, %s, %s)""", (inputs["name"], inputs["type"], inputs["question"], inputs["answer"], assignment))
            except Exception as e:
                inputs["errors"] = e

            return HttpResponse(json.dumps(inputs), content_type="application/json")

    except Exception as e:

        return HttpResponse("Not logged in")


def editQuestion(request, assignment, question):

    try:
        if(request.session["user"]):
            inputs = {"assignment":assignment, "errors":""}

            try:
                inputs["name"] = request.POST["name"]
            except Exception as e:
                inputs["name"] = ""
  
            try:
                inputs["type"] = request.POST["type"]
            except Exception as e:
                inputs["type"] = ""
  
            try:
                inputs["question"] = request.POST["question"]
            except Exception as e:
                inputs["question"] = ""
  
            try:
                inputs["answer"] = request.POST["answer"]
            except Exception as e:
                inputs["answer"] = ""

            try:
                if(len(inputs["question"]) != 0 and len(inputs["answer"]) != 0 and len(inputs["type"]) != 0):
                    db.Query("""UPDATE questions SET `name`=%s, `type`=%s, `question`=%s, `answer`=%s WHERE id=%s AND `assignment`=%s""", (inputs["name"], inputs["type"], inputs["question"], inputs["answer"], question, assignment))
            except Exception as e:
                inputs["errors"] = e

            return HttpResponse(json.dumps(inputs), content_type="application/json")

    except Exception as e:

        return HttpResponse("not loogged in")
