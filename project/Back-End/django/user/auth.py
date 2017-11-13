# -*- coding: utf-8 -*-
import time

from django.http import QueryDict
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from library import database as db
from library import tools

#==================================================================================================

TA_ROLES = ["ta", "admin"]
STUDENT_ROLES = ["student"]

def login(request):
	try:
		if(checkOperator(request)):
			if(request.session["user"]["role"] in TA_ROLES):
					return HttpResponse('<html lang="en"><head><meta http-equiv="refresh" content="0; url=/html/welcomeTA.html"/></head><body>Login success</body></html>')
			elif(request.session["user"]["role"] in STUDENT_ROLES):
					return HttpResponse('<html lang="en"><head><meta http-equiv="refresh" content="0; url=/html/welcome.html"/></head><body>Login success</body></html>')
			else:
				return HttpResponse("Failed to login system, %s" % ex)
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

