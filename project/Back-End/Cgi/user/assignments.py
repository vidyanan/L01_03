# -*- coding: utf-8 -*-

import time
import json
import random

from django.http import QueryDict
from django.http import HttpResponse

from django.conf import settings

from library import database as db
from library import tools

#==============================================================================

CREATE_ROLES = ["ta", "admin"]
EDIT_ROLES = ["admin", "ta"]
GET_ROLES = ["admin", "ta", "student"]
ROOT_HTML = "/home/nginx/www/html/"
MAX_QUESTIONS = 10
REDIRECT_FORM = """<html lang="en">
<head>
<meta http-equiv="refresh" content="0; url={}"/>
</head>
<body>{}</body>
</html>"""

def assembleGradeDict(sqlQuery):

    temp = dict()

    for element in sqlQuery:

        try:
            temp[element["assignment"]] = float(element["grade"])
        except Exception as e:
            temp[element["assignment"]] = float(0.0)

    return temp

def getStudentGrades(userID):

    grades = db.Query(
        """ SELECT grade, a.id AS assignment
            FROM  assignments AS a
                LEFT JOIN
                    (SELECT *
                     FROM grades
                     WHERE user=%s) AS g
                ON a.id=g.assignment""", (userID,))

    return assembleGradeDict(grades)

def getAllGrades():

    grades = db.Query(
        """ SELECT AVG(grade) AS grade, a.id AS assignment
            FROM assignments AS a LEFT JOIN grades AS g
                ON a.id=g.assignment
            GROUP BY a.id""", ())

    return assembleGradeDict(grades)

def getAssignments(request):
    try:
        if(request.session["user"]["role"] in GET_ROLES):
            #return template based on user
            #result = {"errors":""}
            result = dict()
            arrayToAdd = []
            assignments = db.Query(
                """     SELECT *
                        FROM `assignments`
                                """,
                ())

            # assemble the grades before hand so that we reduce SQL queries
            grades = dict()
            if(request.session["user"]["role"] == "ta"):
                grades = getAllGrades();
            elif(request.session["user"]["role"] == "student"):
                grades = getStudentGrades(request.session["user"]["ID"])

            for assignment in assignments:
                temp = dict()
                temp["id"] = assignment["id"]
                temp["name"] = assignment["name"]
                temp["start-date"] = assignment["start-date"]
                temp["end-date"] = assignment["end-date"]
                try:
                    temp["grade"] = "%3.2f" % (grades[assignment["id"]])
                except Exception as e:
                    return HttpResponse(json.dumps(grades), content_type="application/json")
                arrayToAdd.append(temp)
            result["assignments"] = arrayToAdd
            return HttpResponse(json.dumps(result), content_type="application/json")

    except Exception as e:
        return HttpResponse(json.dumps(e), content_type="application/json") 

def createAssignment(request):
    try:
        if(request.session["user"]["role"] in CREATE_ROLES):
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

        #    return HttpResponse(json.dumps(inputs), content_type="application/json")

        
            return HttpResponse(REDIRECT_FORM.format("/html/assignmentlist.html", json.dumps(inputs)))
        

    except Exception as e:
        
        return HttpResponse(e)

def editAssignments(request, assignment):
    try:
        if(request.session["user"]["role"] in EDIT_ROLES):
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

            return  HttpResponse(REDIRECT_FORM.format("/html/assignmentlist.html", json.dumps(inputs)))

    except Exception as e:

        return HttpResponse(e)

def taGetQuestions(request, assignment):
    result = {"errors":"", "assignment":assignment}
    arrayToAdd = []
    fix = str(assignment)
    questions=db.Query("SELECT * FROM `questions` WHERE `assignment`=" + assignment, ())

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

def studentGetQuestions(request, assignment):

    # get a set of questions
    arrayToAdd = []

    # Delete any old answers

    db.Query(
    """    DELETE FROM `answers`
           WHERE `assignment`=%s
           AND `user`=%s""", (assignment, request.session["user"]["ID"]))

    db.Query(
    """    DELETE FROM `grades`
           WHERE `assignment`=%s
           AND `user`=%s""", (assignment, request.session["user"]["ID"]))

    questions = db.Query(
    """    SELECT *
           FROM `questions`
           WHERE `assignment`=%s""", (assignment,))

    # fill in questions into multiple divs
    mc = open(ROOT_HTML + "multipleChoiceTemplate.html", 'r').read()
    sa = open(ROOT_HTML + "shortAnswerTemplate.html", 'r').read()

    for question in questions:
        if(question["type"] == "multiple-choice"):
           # parse answer by splitting strings ';' for end of question ':' for multiple choice
           questionParse = question["question"].split(";")
           multipleChoicePart = questionParse[1].split(":")

           buf = ""

           for multipleChoice in multipleChoicePart:
               buf = buf + '<input type="radio" name="{}:{}">{}<br>'.format(question["id"], multipleChoice, multipleChoice)

           arrayToAdd.append(mc.format(questionParse[0], buf))

        elif(question["type"] == "short-answer"):
           arrayToAdd.append(sa.format(question["question"], question["id"]))
        else:
           arrayToAdd.append("error") 

    # randomize questions
    random.shuffle(arrayToAdd)

    # limit questions
    arrayToAdd = arrayToAdd[:10]

    # put these questions in html
    buf = ""
    for question in arrayToAdd:
        buf = buf + question + '\n'

    finHtml = open(ROOT_HTML + "questionpage.html", 'r').read()

    # pull assignment information
    assignment = db.Query("SELECT * FROM `assignments` WHERE `id`=%s""", (assignment,)).fetch()

    # return html

    return HttpResponse(finHtml.format(assignment["name"], assignment["id"], buf))

def getQuestions(request, assignment):
    try:
        if(request.session["user"]["role"] in GET_ROLES):

            if(request.session["user"]["role"] in EDIT_ROLES or request.session["user"]["role"] in CREATE_ROLES):
                return taGetQuestions(request, assignment)
            else:
                return studentGetQuestions(request, assignment)

    except Exception as e:

        return HttpResponse(e)


def createQuestion(request, assignment):
    try:

        if(request.session["user"]["role"] in CREATE_ROLES):
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
                    """     INSERT INTO `questions` (`name`, `type`, `question`, `answer`, `assignment`)
                            VALUES (%s, %s, %s, %s, %s)""", (inputs["name"], inputs["type"], inputs["question"], inputs["answer"], assignment))
            except Exception as e:
                inputs["errors"] = e

            return HttpResponse(REDIRECT_FORM.format("/{}/questionlist.html".format(assignment), json.dumps(inputs)))

    except Exception as e:

        return HttpResponse(e)


def editQuestion(request, assignment, question):

    try:
        if(request.session["user"]["role"] in EDIT_ROLES):
            inputs = {"assignment":assignment, "errors":"", "raw":request.POST}

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

            return HttpResponse(REDIRECT_FORM.format("/{}/questionlist.html".format(assignment), json.dumps(inputs)))

    except Exception as e:

        return HttpResponse("not loogged in")

def submitQuestion(request, assignment):
    try:
        if(request.session["user"]):
            result = []
            # get keys
            for key in request.POST.keys():
                # if it's a multiple choice question
                if(request.POST[key] == "on"):

                    #split question and answer
                    answer = key.split(":")
                    db.Query(
                        """INSERT INTO answers 
                           (user, assignment, question, answer) 
                           VALUES (%s, %s, %s, %s)""", 
                           (request.session["user"]["ID"], assignment, answer[0], answer[1]))

                # If it's a short answer
                else:
                    db.Query(
                        """INSERT INTO answers
                           (user, assignment, question, answer)
                           VALUES (%s, %s, %s, %s)""",
                           (request.session["user"]["ID"], assignment, key, request.POST[key]))

            # get count of right answers
            count = db.Query(
                """ SELECT COUNT(q.id) AS count, q.assignment
                    FROM questions AS q JOIN answers AS a
                        ON q.id=a.question
                    WHERE user=%s 
                        AND q.answer=a.answer 
                        AND q.assignment=%s""", (request.session["user"]["ID"], assignment)).fetch()

            # get total number of questions in assignment
            total = db.Query(
                """ SELECT COUNT(id) AS count FROM questions WHERE assignment=%s""", (assignment,)).fetch()

            total = float(total["count"]) if float(total["count"]) < MAX_QUESTIONS else MAX_QUESTIONS


            db.Query(""" INSERT INTO grades (user, assignment, grade)
                         VALUES (%s, %s, %s)""", (request.session["user"]["ID"], assignment, float(count["count"])/total*100))
                
            return HttpResponse(REDIRECT_FORM.format("/html/assignmentliststudent.html", json.dumps(result)))
    except Exception as e:
        return HttpResponse(e, content_type="application/json")

def getLeaders(request):

    try:

        grades = db.Query(
        """ SELECT AVG(g.grade) as grade, u.email as name
            FROM (select email, id FROM user) as u JOIN grades as g
                ON u.id = g.user
            GROUP BY u.id
            ORDER BY grade DESC""", ())


        # assemble the return value
        result = []
        for row in grades:
            temp = dict()
            temp["user"] = row["name"]
            temp["grade"] = row["grade"]
            result.append(temp)

        return HttpResponse(json.dumps(result), content_type="application/json")

    except Exception as e:
        return HttpResponse(json.dumps(e), content_type="application/json")

