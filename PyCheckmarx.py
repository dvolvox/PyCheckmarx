#!usr/bin/python

###############################
# > Author: Duarte Monteiro
# > Version: 1.0
# > Vendor: www.checkmarx.com
# > Notes: Python API for Checkmarx WSDL
###############################

# Python Dependencies
from suds.client import Client
from suds.sudsobject import asdict
import base64
import re
import json
import time

class PyCheckmarx(object):

	# Internal Variables for the Class
	DEBUG = False
	configPath = "etc/"
	errorLog = []
	ttlReport = 6
	timeWaitReport = 3  

	#
	# Init Function
	#
	def __init__(self):
		# Get Configuration
		self.getConfig()
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
	def getProjectScannedDisplayData(self, filterOn=False):
		tmp = self.client.service.GetProjectScannedDisplayData(self.sessionId)

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		if not filterOn:
			return self.convertToJson(tmp)
		else:
			return tmp.ProjectScannedList[0]

	#
	# Get Project Display Data
	# 
	def getProjectsDisplayData(self, filterOn=False):
		tmp = self.client.service.GetProjectsDisplayData(self.sessionId)

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		if not filterOn:
			return self.convertToJson(tmp)
		else:
			return tmp.projectList[0]

	#
	# Get Scan Info For All Projects
	#
	def getScanInfoForAllProjects(self, filterOn=False):
		tmp = self.client.service.GetScansDisplayDataForAllProjects(self.sessionId)
		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)


		if not filterOn:
			return self.convertToJson(tmp)
		else:
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

		return self.convertToJson(tmp)

	#
	# Get Configuration List
	#
	def getConfigurationList(self):
		tmp = self.client.service.GetConfigurationSetList(self.sessionId)

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return self.convertToJson(tmp)

	#
	# Get Associated Groups List 
	#	
	def getAssociatedGroups(self):
		tmp = self.client.service.GetAssociatedGroupsList(self.sessionId)

		if not tmp.IsSuccesfull:
			raise Exception("Unable to get data from the server.")

		if self.DEBUG:
			print dir(tmp)

		return self.convertToJson(tmp)

	#
	# Filter For [getProjectScannedDisplayData]
	# 
	def filterProjectScannedDisplayData(self, projectID):
		tmpProjects = self.getProjectScannedDisplayData(True)
		for project in tmpProjects:
			if project.ProjectID == projectID:
				return self.convertToJson(project)

		raise Exception("Could not find ProjectID: %s " % projectID)

	#
	# Filter for [getProjectsDisplayData]
	#
	def filterProjectsDisplayData(self,projectID):
		tmpProjects = self.getProjectsDisplayData(True)
		for project in tmpProjects:
			if project.projectID == projectID:
				return self.convertToJson(project)

		raise Exception("Could not find ProjectID: %s " % projectID)
	
	#
	# Filter for [getScanInfoForAllProjects]
	#
	def filterScanInfoForAllProjects(self,projectID):
		tmpProjects = self.getScanInfoForAllProjects(True).ScanList[0]
		for project in tmpProjects:
			if project.ProjectId == projectID:
				return self.convertToJson(project)

		raise Exception("Could not find ProjectID: %s " % projectID)

	#
	# Get Suppressed Issues
	#
	def getSupressedIssues(self, scanID):
		CxWSReportType = self.client.factory.create("CxWSReportType")
		CxReportRequest = self.client.factory.create("CxWSReportRequest")
		CxReportRequest.ScanID = scanID
		CxReportRequest.Type = CxWSReportType.XML
		createReportResponse = self.client.service.CreateScanReport(self.sessionId, CxReportRequest)
		if createReportResponse.IsSuccesfull:

			if self.DEBUG:
				print createReportResponse
				print "Success. Creating Get Scan Report Status"

			inc = 0
			while inc < self.ttlReport:
				inc += 1
				reportStatusResponse = self.client.service.GetScanReportStatus(self.sessionId, createReportResponse.ID)
				if reportStatusResponse.IsSuccesfull and  reportStatusResponse.IsReady:
					break

				if self.DEBUG:
					print "fail"
				time.sleep(self.timeWaitReport)

			if self.DEBUG:
				print "Sucess. Creating Get Scan Report"
			responseScanResults = self.client.service.GetScanReport(self.sessionId, createReportResponse.ID )

			if responseScanResults.IsSuccesfull and responseScanResults.ScanResults:

				XMLData = base64.b64decode(responseScanResults.ScanResults)

				issues = re.findall('FalsePositive="([a-zA-Z]+)" Severity="([a-zA-Z]+)"', XMLData)
				
				if self.DEBUG:
					print responseScanResults
					print issues

				mediumSupressIssues = 0
				lowSupressIssues = 0
				highSupressIssues = 0
				otherSupressIssues = 0

				for a,b in issues:
					if a == "True":
						if b == "Medium":
							mediumSupressIssues += 1
						elif b == "High":
							highSupressIssues += 1
						elif b == "Low":
							lowSupressIssues += 1
						else:
							otherSupressIssues += 1
				if self.DEBUG:
					print highSupressIssues
					print mediumSupressIssues
					print lowSupressIssues
				return {"highSupressIssues": highSupressIssues, "mediumSupressIssues": mediumSupressIssues, "lowSupressIssues": lowSupressIssues}
			else:
				raise Exception("Unable to Get Report")

		else:
			raise Exception("Unable to get Supressed")      

	#
	# Convert Suds object into serializable format.
	#
	def recursive_asdict(self,d):
		out = {}
		for k, v in asdict(d).iteritems():
			if hasattr(v, '__keylist__'):
				out[k] = self.recursive_asdict(v)
			elif isinstance(v, list):
				out[k] = []
				for item in v:
					if hasattr(item, '__keylist__'):
						out[k].append(self.recursive_asdict(item))
					else:
						out[k].append(item)
			else:
				out[k] = v
		return out


	#
	# Return Subs Object into Serializable format Handler
	#
	def convertToJson(self, data):
		try:
			tmp = self.recursive_asdict(data)
			return json.dumps(tmp)
		except Exception as e:
			raise Exception("Unable to convert to JSON: %s" % e.message)


##########################################
#
# Testing AREA
#
##########################################

#tmp = PyCheckmarx()
#print tmp.filterProjectScannedDisplayData(20004)
#print tmp.getSupressedIssues("1000004")

