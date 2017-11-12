# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from user import auth, me, userAccounts, redirect
from user import assignments
from index import index

urlpatterns = patterns('',
    #Global level urls
    url(r'^$',							index.view,				name='indexView'),
    url(r'^login/$',					auth.login,				name='login'),
    url(r'^logout/$',					auth.logout,					name='logout'),
    url(r'^me/$',						me.me,				name='showMe'),
    url(r'^assignments/get/$',                          assignments.getAssignments,                     name='getAssignments'),
    url(r'^assignments/$',                              assignments.createAssignment,           name='createAssignment'),
    url(r'^assignments/([0-9]*)/edit/$',                assignments.editAssignments,                    name='editAssignments'),
    url(r'^assignments/([0-9]*)/get/$',                 assignments.getQuestions,               name='getQuestions'),
    url(r'^assignments/([0-9]*)/$',                     assignments.createQuestion,                     name='createQuestion'),
    url(r'^assignments/([0-9]*)/([0-9]*)/$',            assignments.editQuestion,               name="editQuestion"),
    url(r'^assignments/([0-9]*)/submit/$',		assignments.submitQuestion,			name='submitQuestion'),
    url(r'^account/student/$',                           	userAccounts.createStudent,	name='createStudents'),
    url(r'^account/ta/$',					userAccounts.createTA,			name='createTA'),
    url(r'^html/toBEFILLED.html$',                      redirect.getSingleAssignment,           name='getSingleAssignment'),

    url(r'^admin/',						include('cgi.admin.urls')),
)
