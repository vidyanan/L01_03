# -*- coding: utf-8 -*-

import time
import MySQLdb
import MySQLdb.cursors
from django.conf import settings

#==================================================================================================
class Query(object):
	def __init__(self, sql, args = None):
		global dbConn
		self.sql = sql
		self.args = args
		self.secondTry = False
		while(1):
			if(dbConn is None):
				connectDatabase()
			try:
				self.cursor = dbConn.cursor()
				self.cursor.execute(self.sql, self.args)
				break
			except MySQLdb.Warning:					#Don't why, cannot ignore the warning :(
				break
			except MySQLdb.Error as ex:
				if(ex[0]<2000 or self.secondTry):	#Server error or the second try
					raise RuntimeError("Execute SQL error %s: %s"%(ex, sql))
				self.closeConnection()				#Client error or first try
				self.secondTry = True				#Close the connection and try again
			except Exception as e:
				self.closeConnection()				#Unknown exception, reset database connection
				raise RuntimeError("Run SQL unknown error %s: %s"%(e, sql))
	#----------------------------------------------------------------------------------------------
	def __iter__(self):
		return self
	#----------------------------------------------------------------------------------------------
	def next(self):
		row = self.cursor.fetchone()
		if(row is None):
			raise StopIteration
		return row
	#----------------------------------------------------------------------------------------------
	def fetch(self):
		return self.cursor.fetchone()
	#----------------------------------------------------------------------------------------------
	def fetchAll(self):
		return self.cursor.fetchall()
	#----------------------------------------------------------------------------------------------
	def fields(self):
		return tuple([i[0] for i in self.cursor.description])
	#----------------------------------------------------------------------------------------------
	def id(self):
		return dbConn.insert_id()
	#----------------------------------------------------------------------------------------------
	def len(self):
		return self.cursor.rowcount
	#----------------------------------------------------------------------------------------------
	def __len__(self):
		return self.cursor.rowcount
	#----------------------------------------------------------------------------------------------
	def closeConnection(self):
		global dbConn
		try:
			dbConn.close()
		except:
			pass
		finally:
			dbConn = None

#==================================================================================================
dbConn = None
CFG = settings.DATABASES['default']
HOST = {'host' : CFG['HOST'],
		'user' : CFG['USER'],
		'passwd' : CFG['PASSWORD'],
		'db' : CFG['NAME'],
		'cursorclass' : MySQLdb.cursors.DictCursor,
		'charset' : 'utf8',
		'use_unicode' : True }
if (CFG['HOST'] != 'localhost' and CFG['PORT']):
	HOST['port'] = int(ICS.database.port)

#==================================================================================================
def connectDatabase():
	global dbConn
	try:
		dbConn.close()
	except Exception, ex:
		pass
	dbConn = MySQLdb.connect(**HOST)
	dbConn.autocommit(1)



