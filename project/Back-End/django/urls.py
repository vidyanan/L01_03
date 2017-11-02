# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from user import auth, me
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

    url(r'^admin/',						include('cgi.admin.urls')),
)
