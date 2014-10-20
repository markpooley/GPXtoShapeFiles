import os
import arcpy
import csv

#Script takes attribute table from a user specified shapefile and exports it directly to
#a user defined directory with a user defined name

GPXPoints = arcpy.GetParameterAsText(0)
LineFC = arcpy.GetParameterAsText(1)
OriginFC = arcpy.GetParameterAsText(2)
DestinationFC = arcpy.GetParameterAsText(3)

workspace = "C:\\Users\\mpooley\\Documents\\ArcGIS\\Projects\\Bicycle Research\\Scratch.gdb"
GPXFileList = [name for name in os.listdir(GPXPoints)]
Featurecount = len(GPXFileList)
counter = 0

arcpy.SetProgressor("step","Converting and appending GPS data....",0,int(Featurecount),1)
for item in GPXFileList:
	item = os.path.join(GPXPoints,item)
	OutputName = "Temp_TripPoints" 
	GPXtoFeature = arcpy.GPXtoFeatures_conversion(item,OutputName)
	counter += 1
	
	arcpy.SetProgressorLabel("Finding Trip Origin and appending it to Origin Feature Class...")
	FeatureLayer = arcpy.MakeFeatureLayer_management(GPXtoFeature,"TempLayer")
	Origin_SelectionClause = "OBJECTID = " + str(1)
	OriginSelction = arcpy.Select_analysis(GPXtoFeature,"TripOrigin",Origin_SelectionClause)
	arcpy.Append_management(OriginSelction,OriginFC,"TEST", "#", "#")

	arcpy.SetProgressorLabel("Finding Trip Destination and appending it to Destination Feature Class...")
	RowCount = int(arcpy.GetCount_management(GPXtoFeature).getOutput(0))
	Destination_SelectionClause = "OBJECTID = " + str(RowCount)
	DestinationSelection = arcpy.Select_analysis(GPXtoFeature,"TripDestination",Destination_SelectionClause)
	arcpy.Append_management(DestinationSelection,DestinationFC,"TEST", "#", "#")


	LineName = "Temp_TripLine"
	TripLine = arcpy.PointsToLine_management(GPXtoFeature,LineName,"Name","#","NO_CLOSE")

	TripLines = arcpy.Append_management(TripLine,LineFC,"TEST","#","#")

	arcpy.SetProgressorPosition()
