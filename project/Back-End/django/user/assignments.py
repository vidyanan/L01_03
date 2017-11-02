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
            assignments = {"a1":{"id":1, "name":"assignment1", "start-date":"2016-06-13", "end-date":"2019-03-11"}, "a2":{"id":2, "name":"assignment2", "start-date":"2011-01-14", "end-date":"2013-04-20"}, "errors":""}
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
        
        return HttpResponse("Not logged in")

def getQuestions(request, assignment):
    try:
        if(request.session["user"]):
            questions = {"assignment":assignment, "q1":{"id":1, "name":"question1", "type":"multiple-choice", "question":"hello world?", "answer":"hello very much so"}, "q2":{"id":2, "name":"question2", "type":"short-answer", "question":"hello world2?", "answer":"answer2"}, "errors":""}

            return HttpResponse(json.dumps(questions), content_type="application/json")

    except Exception as e:

        return HttpResponse("Not logged in")


def createQuestion(request, assignment):
    try:

        if(request.session["user"]):
            inputs = {"assignment":assignment, "errors":""}

            try:
                inputs["name"] = request.POST["name"]
            except Exception as e:
                inputs["name"] = "ERROR COULD NOT FIND"

            try:
                inputs["type"] = request.POST["type"] 
            except Exception as e:
                inputs["type"] = "ERROR COULD NOT FIND"

            try:
                inputs["question"] = request.POST["question"]
            except Exception as e:
                inputs["question"] = "ERROR COULD NOT FIND"

            try:
                inputs["answer"] = request.POST["name"]
            except Exception as e:
                inputs["answer"] = "ERROR COULD NOT FIND"

            return HttpResponse(json.dumps(inputs), content_type="application/json")

    except Exception as e:

        return HttpResponse("Not logged in")


def editQuestion(request, assignment, question):

    try:

        if(request.session["user"]):
            inputs = {"assignment":assignment, "questionID":question, "errors":""}

            try:
                inputs["name"] = request.POST["name"]
            except Exception as e:
                inputs["name"] = "ERROR COULD NOT FIND"

            try:
                inputs["type"] = request.POST["type"]
            except Exception as e:
                inputs["type"] = "ERROR COULD NOT FIND"

            try:
                inputs["question"] = request.POST["question"]
            except Exception as e:
                inputs["question"] = "ERROR COULD NOT FIND"

            try:
                inputs["answer"] = request.POST["name"]
            except Exception as e:
                inputs["answer"] = "ERROR COULD NOT FIND"

            return HttpResponse(json.dumps(inputs), content_type="application/json")

    except Exception as e:

        return HttpResponse("Not logged in")
