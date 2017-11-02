# -*- coding: utf-8 -*-

import os
import json
import datetime
import decimal
from operator import itemgetter
from lxml import etree

from django.http import HttpResponse
from django.conf import settings
try:
	from django.core.servers.basehttp import FileWrapper
except:
	from wsgiref.util import FileWrapper

import database as db

#--------------------------------------------------------------------------------------------------
def multiKeySort(items, keys):
	keys = [keys] if(type(keys) == str) else keys
	comparers = [((itemgetter(key[1:].strip()), -1) if key.startswith('-') \
		else (itemgetter(key.strip()), 1)) for key in keys]
	def comparer(left, right):
		for fn, mult in comparers:
			result = cmp(fn(left), fn(right))
			if result:
				return mult * result
		else:
			return 0
	return sorted(items, cmp=comparer)

#--------------------------------------------------------------------------------------------------
#The response object for ICS.request()
def response(errno, message, **args):
	root = etree.Element("response", dict2xmlattr(args))
	root.set('errno', str(errno))
	root.text = message
	response = HttpResponse(etree.tostring(root, xml_declaration=True, encoding="UTF-8"))
	response['Cache-Control'] = 'no-cache, must-revalidate'
	response['Content-Type'] = 'text/xml'
	return response

#--------------------------------------------------------------------------------------------------
def sendFile(fileObj, **header):
	wrapper = FileWrapper(file(fileObj) if(type(fileObj) == str) else fileObj)
	response = HttpResponse(wrapper,
		content_type=header.get('content_type', header.get('Content-Type')))
	for key, value in header.iteritems():
		response[key] = value
	fileObj.seek(0, 2)								#Used to get file size
	response['Content-Length'] = fileObj.tell()
	fileObj.seek(0)
	return response

#--------------------------------------------------------------------------------------------------
def nl2br(string):
	return '<br />\n'.join(string.split('\n'))

#--------------------------------------------------------------------------------------------------
def htmlEscape(string):
	string = string.replace("&", "&amp;").replace("<", "&lt;").replace("'", "&apos;")
	return string.replace('"', "&quot;").replace(">", "&gt;")

#--------------------------------------------------------------------------------------------------
def htmlUnescape(s):
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	s = s.replace("&amp;", "&")
	return s

#--------------------------------------------------------------------------------------------------
def multipleReplace(sText, dWord):
	for key, value in dWord.items():
		sText = sText.replace(key, value)
	return sText

#--------------------------------------------------------------------------------------------------
def escape(string):
	return string.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'") \
		if(type(string) in (str, unicode)) else str(string)

#--------------------------------------------------------------------------------------------------
__TRUE = set(['yes', 'true', 'ok', 'on'])
__FALSE = set(['no', 'false', 'off'])
def str2bool(string, dft=False):
	try:
		string = string.lower()
		return True if(string in __TRUE) else (False if(string in __FALSE) else dft)
	except:
		return dft
parseBool = str2bool

#--------------------------------------------------------------------------------------------------
def str2float(string, dflt=None):
	try:
		return float(string)
	except Exception as ex:
		return dflt
parseFloat = str2float

#--------------------------------------------------------------------------------------------------
def str2int(string, dflt=None):
	try:
		return int(str2float(string, dflt))
	except Exception as ex:
		return dflt
parseInt = str2int

#--------------------------------------------------------------------------------------------------
def isFloat(value):
	try:
		float(value)
		return True
	except:
		return False


#--------------------------------------------------------------------------------------------------
class jsonEncoder(json.JSONEncoder):
	def __init__(self, nan_str="null", **kwargs):
		super(icsJsonEncoder, self).__init__(**kwargs)
		self.nan_str = nan_str
	#----------------------------------------------------------------------------------------------
	def default(self, obj):
		if(isinstance(obj, datetime.datetime)):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif(isinstance(obj, datetime.date)):
			return obj.strftime('%Y-%m-%d')
		elif(isinstance(obj, decimal.Decimal)):
			return float(obj)
		raise TypeError(repr(obj) + " is not JSON serializable")
	#----------------------------------------------------------------------------------------------
	def iterencode(self, o, _one_shot=False):
		"""Encode the given object and yield each string
		representation as available.
		For example::
			for chunk in JSONEncoder().iterencode(bigobject):
				mysocket.write(chunk)
		"""
		if self.check_circular:
			markers = {}
		else:
			markers = None
		if self.ensure_ascii:
			_encoder = json.encoder.encode_basestring_ascii
		else:
			_encoder = json.encoder.encode_basestring
		if self.encoding != 'utf-8':
			def _encoder(o, _orig_encoder=_encoder, _encoding=self.encoding):
				if isinstance(o, str):
					o = o.decode(_encoding)
				return _orig_encoder(o)
		#------------------------------------------------------------------------------------------
		def floatstr(o, allow_nan=self.allow_nan, _repr=json.encoder.FLOAT_REPR,
				_inf=json.encoder.INFINITY, _neginf=-json.encoder.INFINITY,
				nan_str=self.nan_str):
			# Check for specials.  Note that this type of test is processor
			# and/or platform-specific, so do tests which don't depend on the
			# internals.
			if o != o:
				text = nan_str
			elif o == _inf:
				text = nan_str
			elif o == _neginf:
				text = nan_str
			else:
				return _repr(o)
			if not allow_nan:
				raise ValueError(
					"Out of range float values are not JSON compliant: " +
					repr(o))
			return text
		#------------------------------------------------------------------------------------------
		_iterencode = json.encoder._make_iterencode(
				markers, self.default, _encoder, self.indent, floatstr,
				self.key_separator, self.item_separator, self.sort_keys,
				self.skipkeys, _one_shot)
		return _iterencode(o, 0)

