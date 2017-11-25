# -*- coding: utf-8 -*-

from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

def view(request):
	return HttpResponse("Hallow world")
