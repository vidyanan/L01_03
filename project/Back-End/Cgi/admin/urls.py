# -*- coding: utf-8 -*-
MODULE_VERSION = "$Revision: 598 $"
MODULE_DATE = "$Date: 2016-08-08 17:53:16 +0000 (Mon, 08 Aug 2016) $"

from django.conf.urls import patterns, include, url
import admin

urlpatterns = patterns('',
	#----------------------------------------------------------------------------------------------
	url(r'^$',								admin.view),
)
 
