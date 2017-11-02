# -*- coding: utf-8 -*-
import time

from django.http import QueryDict
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from library import database as db
from library import tools

#==================================================================================================
def login(request):
	try:
		if(checkOperator(request)):
			return HttpResponse('Login success')
		else:
			time.sleep(2)
			return HttpResponse('Invalid user or password')
	except Exception as ex:
		return HttpResponse("Failed to login system, %s" % ex)

#==================================================================================================
def logout(request):
	request.session.clear()
	return HttpResponseRedirect(settings.LOGIN_URL)

#--------------------------------------------------------------------------------------------------
def checkOperator(request):
	"""
	Check user authority
	"""
	# Clear expired sessions
	db.Query("DELETE FROM `django_session` WHERE `expire_date`<NOW()")
	# Load user
	usr = db.Query(
		"""	SELECT *
			FROM `user`
			WHERE `email`=%s
				AND `password`=MD5(%s)
				AND `enabled`='Yes'""",
		(request.POST["email"], request.POST["password"])).fetch()
	# Check authority
	if(usr):
		usr.pop('last_login')
		usr.pop('password')
		request.session["user"] = usr
		request.session["isLogin"] = True
		request.session.set_expiry(settings.SESSION_TIMEOUT)
		db.Query("UPDATE `user` SET `last_login`=NOW() WHERE `ID`=%s", (usr['ID'], ))
		return True
	return False

