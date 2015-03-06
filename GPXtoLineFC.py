# !/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Name          : GPX to Line FC.py
# Author  		: Mark Pooley (mark-pooley@uiowa.edu)
# Link    		: http://www.ppc.uiowa.edu
# Date    		: 2014-9-06 09:49:45
# Version		: $1.0$
# Description	: Takes a folder of GPX data from a GPS and converts tracks to lines. Additionally,
# it appends Origins and Destinations to separate feature classes. User needs to create a Line,
# Origin, and Destination Feature class prior to running script so each file can be appended to
# them easily. When creating the Feature Classes, create an attribute that will have the same
# attributes/names as the input GPX data.
#-------------------------------------------------------------------------------------------------

###################################################################################################
#Import python modules
###################################################################################################
import os
import arcpy
import csv

###################################################################################################
#Input Variable loading and environment declaration
###################################################################################################
GPXPoints = arcpy.GetParameterAsText(0)
LineFC = arcpy.GetParameterAsText(1)
OriginFC = arcpy.GetParameterAsText(2)
DestinationFC = arcpy.GetParameterAsText(3)

###################################################################################################
# Defining global functions
###################################################################################################

###################################################################################################
#Global variables to be used in process
###################################################################################################
workspace = os.path.dirname(LineFC) #just put stuff in the same directory as the Line FC
GPXFileList = [name for name in os.listdir(GPXPoints)] #list of gpx data files
Featurecount = len(GPXFileList) #get a feature count


###################################################################################################
#Iterate through GPX files and create Line, Origin, and Destination feature classes
###################################################################################################
arcpy.SetProgressor("step","Converting and appending GPS data....",0,int(Featurecount),1)
for item in GPXFileList:

	#Create points from GPX features
	#---------------------------------------------------------------------------
	item = os.path.join(GPXPoints,item)
	OutputName = "Temp_TripPoints"
	GPXtoFeature = arcpy.GPXtoFeatures_conversion(item,OutputName)

	#Find origin and append it to the Origin Feature Class
	#---------------------------------------------------------------------------
	arcpy.SetProgressorLabel("Finding Trip Origin and appending it to Origin Feature Class...")
	FeatureLayer = arcpy.MakeFeatureLayer_management(GPXtoFeature,"TempLayer")
	Origin_SelectionClause = "OBJECTID = " + str(1)
	OriginSelction = arcpy.Select_analysis(GPXtoFeature,"Temp_TripOrigin",Origin_SelectionClause)
	arcpy.Append_management(OriginSelction,OriginFC,"TEST", "#", "#")

	#Find desintaiton and append it to the Destination Feature Class
	#---------------------------------------------------------------------------
	arcpy.SetProgressorLabel("Finding Trip Destination and appending it to Destination Feature Class...")
	RowCount = int(arcpy.GetCount_management(GPXtoFeature).getOutput(0)) #get row count
	Destination_SelectionClause = "OBJECTID = " + str(RowCount) #last row is the destination
	DestinationSelection = arcpy.Select_analysis(GPXtoFeature,"Temp_TripDestination",Destination_SelectionClause)
	arcpy.Append_management(DestinationSelection,DestinationFC,"TEST", "#", "#")

	#Create line from GPX points, and append it the trip/line feature class
	#---------------------------------------------------------------------------
	LineName = "Temp_TripLine"
	TripLine = arcpy.PointsToLine_management(GPXtoFeature,LineName,"Name","#","NO_CLOSE")

	TripLines = arcpy.Append_management(TripLine,LineFC,"TEST","#","#")

	arcpy.SetProgressorPosition()


###################################################################################################
#Delete Temporary Files
###################################################################################################
TempFeatures = arcpy.ListFeatureClasses('Temp*')
arcpy.AddMessage('{0} features found to be deleted...'.format(len(TempFeatures)))
for fc in TempFeatures:
	arcpy.Delete_management(fc)

###################################################################################################
#Final Output and cleaning of temp data/variables
###################################################################################################

arcpy.AddMessage("Process complete!")