#!usr/bin/python

###############################
# > Author: Duarte Monteiro
# > Version: 1.0
# > Vendor: www.checkmarx.com
# > Notes: Python API for Checkmarx WSDL
###############################

# Python Dependencies
from suds.client import Client
import json

class PyCheckmarx(object):

	# Internal Variables for the Class
	DEBUG = False
	configPath = "etc/"
	errorLog = []

	#
	# Init Function
	#
	def __init__(self):
		# Get Configuration
		self.getConfig()
		print self.USERNAME
		print self.PASSWORD
		# Open Connection With Checkmarx
		self.Initclient = self.openConnection()
		# Get the Service URL
		self.serviceUrl = self.getServiceUrl(self.Initclient)
		# Get the Session Id and Client Object
		(self.sessionId, self.client) = self.getSessionId(self.Initclient,self.serviceUrl)
		return None

	##########################################
	#
	# Functions Related to Openning session with Checkmarx
	#
	##########################################

	#
	# Get Configuration
	#
	def getConfig(self):
		try:
			with open(self.configPath + "config.json", "r") as outfile:
				tmpJson = json.load(outfile)["checkmarx"]
				self.USERNAME = str(tmpJson["username"])
				self.PASSWORD = str(tmpJson["password"])
				self.URL = str(tmpJson["url"])
				self.APITYPE = tmpJson["APIType"]
		except Exception as e:
			raise Exception("Unable to get configuration: %s" % e.message)

	#
	# Open Connection
	#
	def openConnection(self):
		try:
			tmpClient = Client(self.URL)
			if self.DEBUG:
				print dir(tmpClient)
			return tmpClient	
		except Exception as e:
			raise Exception("Unable to establish connection with WSDL [%s]: %s " % (self.URL, e.message))

	#
	# Get Service URL
	#
	def getServiceUrl(self, client):
		try:
			CxClient = client.factory.create('CxClientType')
			responseDiscovery = client.service.GetWebServiceUrl(CxClient.SDK,self.APITYPE)

			if responseDiscovery.IsSuccesfull:
				serviceUrl = responseDiscovery.ServiceURL
			else:
				raise Exception("Error establishing connection > %s" % cxSDK.ErrorMessage)

			if self.DEBUG:
				print "Response Discovery Object:", dir(responseDiscovery)
				print "Service Url:", serviceUrl

			return serviceUrl
		except Exception as e:
			raise Exception("Unable to get Service URL: %s" % e.message)

	#
	# Login in Checkmarx and retrive the Session ID
	#
	def getSessionId(self,client, serviceUrl): 
		try:
			clientSDK = Client(serviceUrl + "?wsdl")

			CxLogin = clientSDK.factory.create("Credentials")
			CxLogin.User = self.USERNAME
			CxLogin.Pass = self.PASSWORD

			cxSDK = clientSDK.service.Login(CxLogin,1033)

			if not cxSDK.IsSuccesfull:
				raise Exception("Unable to Login > %s" % cxSDK.ErrorMessage)

			if self.DEBUG:
				print "Service Object:", dir(client)
				print "Login Object:", dir(cxSDK)
				print "Session ID:", cxSDK.SessionId

			return (cxSDK.SessionId, clientSDK)
		except Exception as e:
			raise Exception("Unable to get SessionId from [%s] : %s" % (serviceUrl,e.message))

	##########################################
	#
	# Functions Related to the functionality of the WSDL
	#
	##########################################	

	#
	# Get data from the Projects
	#
	def getProjectScannedDisplayData(self):
		tmp = self.client.service.GetProjectScannedDisplayData(self.sessionId).ProjectScannedList[0]
		
		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return tmp

	#
	# Get Project Display Data
	# 
	def getProjectsDisplayData(self):
		tmp = self.client.service.GetProjectsDisplayData(self.SessionId).projectList[0]

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return tmp

	#
	# Get Scan Info For All Projects
	#
	def getScanInfoForAllProjects(self):
		tmp = self.client.service.GetScansDisplayDataForAllProjects(self.sessionId).ProjectScannedList[0]

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return tmp

	#
	# Get Preset List
	#
	def getPresetList(self):
		tmp = self.client.service.GetPresetList(self.sessionId)

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return tmp

	#
	# Get Configuration List
	#
	def getConfigurationList(self):
		tmp = self.client.service.GetConfigurationSetList(self.sessionId)

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return tmp

	#
	# Get Associated Groups List 
	#	
	def getAssociatedGroups(self):
		tmp = self.client.service.GetAssociatedGroupsList(self.sessionId)

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return tmp

	#
	# Filter For [getProjectScannedDisplayData]
	# 
	def filterProjectScannedDisplayData(self, projectID):
		tmpProjects = getProjectScannedDisplayData()
		for project in tmpProjects:
			if project.projectID == projectID:
				return project

		raise Exception("Could not find ProjectID: %s " % projectID)

	#
	# Filter for [getProjectsDisplayData]
	#
	def filterProjectsDisplayData(self,projectID):
		tmpProjects = getProjectsDisplayData()
		for project in tmpProjects:
			if project.projectID == projectID:
				return project

		raise Exception("Could not find ProjectID: %s " % projectID)
	
	#
	# Filter for [getScanInfoForAllProjects]
	#
	def filterScanInfoForAllProjects(self,projectID):
		tmpProjects = getScanInfoForAllProjects()
		for project in tmpProjects:
			if project.projectID == projectID:
				return project

		raise Exception("Could not find ProjectID: %s " % projectID)
