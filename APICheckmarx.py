#!usr/bin/python

###############################
# > Author: Duarte Monteiro
# > Version: 1.0
# > Vendor: www.checkmarx.com
# > Notes: RESTAPI for PyCheckMarx
###############################

# Python Dependencies
from flask import Flask, jsonify, request
app = Flask(__name__)

# Import PyCheckMarx
import PyCheckmarx

#
# Launch error to the user
#
def launchError(message):
	return jsonify({"error":"%s" % message}), 500

#
# getProjectScannedDisplayData
#
@app.route('/APICX/getProjectScannedDisplayData/', methods=["GET"])
@app.route('/APICX/getProjectScannedDisplayData/', defaults={"extra_path": ""}, methods=["GET"])
@app.route('/APICX/getProjectScannedDisplayData/<int:projectID>', methods=["GET"])
def ProjectScannedDisplayData(projectID=None):
	try:
		if projectID == None:
			return pyC.getProjectScannedDisplayData()
		else:
			return pyC.filterProjectScannedDisplayData(projectID)
	except Exception as e:
		return launchError(e.message)

#
# getProjectsDisplayData
#
@app.route('/APICX/getProjectsDisplayData/', methods=["GET"])
@app.route('/APICX/getProjectsDisplayData/<int:projectID>', methods=["GET"])
def ProjectsDisplayData(projectID=None):
	try:
		if projectID == None:
			return pyC.getProjectsDisplayData()
		else:
			return pyC.filterProjectsDisplayData(projectID)
	except Exception as e:
		return launchError(e.message)

#
# getScanInfoForAllProjects
#
@app.route('/APICX/getScanInfoForAllProjects/', methods=["GET"])
@app.route('/APICX/getScanInfoForAllProjects/<int:projectID>', methods=["GET"])
def ScanInfoForAllProjects(projectID=None):
	try:
		if projectID == None:
			return pyC.getScanInfoForAllProjects()
		else:
			return pyC.filterScanInfoForAllProjects(projectID)
	except Exception as e:
		return launchError(e.message)

#
# getPresetList
#
@app.route('/APICX/getPresetList/', methods=["GET"])
def PresetList():
	try:
		return pyC.getPresetList()
	except Exception as e:
		return launchError(e.message)

#
# getConfigurationList
#
@app.route('/APICX/getConfigurationList/', methods=["GET"])
def ConfigurationList():
	try:
		return pyC.getConfigurationList()
	except Exception as e:
		return launchError(e.message)

#
# getAssociatedGroups
#
@app.route('/APICX/getAssociatedGroups/', methods=["GET"])
def AssociatedGroups():
	try:
		return pyC.getAssociatedGroups()
	except Exception as e:
		return launchError(e.message)

#
# Trigger Flask App
#
if __name__ == '__main__':
    print ("[SYS]\tLoading...")
    pyC = PyCheckmarx.PyCheckmarx()
    print ("[SYS]\tLoaded!")
    app.run(debug=True, host="0.0.0.0", port=5000)
