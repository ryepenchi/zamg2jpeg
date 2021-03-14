#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 11:44:33 2020

LV: 2020W 290065-1 Grundlagen der Softwareentwicklung
ausführbar in jedem leeren Projekt,
optionale Parameter:
0   Layout File
"""
# imports
import requests, os, datetime, time

# download of daily (last 24h) earthquake data from ZAMG
# alternative file types: csv
# alternative time periods: lastweek, lastmonth
url = "http://geoweb.zamg.ac.at/static/event/lastday.json"
r = requests.get(url)
with open("lastday.json", "wb") as f:
    f.write(r.content)

# priming work with ArcGIS Pro 2.4 Project File
p = arcpy.mp.ArcGISProject("CURRENT")

# arcpy Function converts json to Feature Layer. reason for choosing json over csv
arcpy.JSONToFeatures_conversion("lastday.json", os.path.join(p.defaultGeodatabase, "quakes"))

# Data Field calculations / type conversion for later use in Symbology
arcpy.management.AddField('quakes', 'Magnitude', 'DOUBLE', '', '', '', 'Magnitude', '', '', '')
expression = "try2float(!mag!)"
code_block = """
def try2float(mag):
    if mag == "-":
        return 0
    else:
        return float(mag)"""
arcpy.management.CalculateField('quakes', 'Magnitude', expression, 'PYTHON3', code_block)

# Check whether to use specific or local Layout File, download if none exists
# Parameter 0 -> localLayout
if arcpy.GetParameterAsText(0):
    arcpy.AddMessage("Using specified Layout File...")
    layout = arcpy.GetParameter(0)
elif not os.path.exists("Layout.pagx"):
    arcpy.AddMessage("Downloading Layout File...")
    url = "https://raw.githubusercontent.com/ryepenchi/zamg2jpeg/main/Layout.pagx"
    r = requests.get(url)
    with open("Layout.pagx", "wb") as f:
        f.write(r.content)
    layout = os.path.join(p.homeFolder, "Layout.pagx")
else:
    arcpy.AddMessage("Using local Layout file...")
    layout = os.path.join(p.homeFolder, "Layout.pagx")
p.importDocument(layout)
lyt = p.listLayouts("Layout")[0]

# Defining the Layer
lyt.listElements("MAPFRAME_ELEMENT")[0].map.addDataFromPath(os.path.join(p.defaultGeodatabase, "quakes"))
lyr = lyt.listElements("MAPFRAME_ELEMENT")[0].map.listLayers("quakes")[0]

# Einige manuelle Einstellungen der Symbology
sym = lyr.symbology
sym.updateRenderer('GraduatedSymbolsRenderer')
sym.renderer.classificationField = 'Magnitude'
sym.renderer.normalizationField = None
sym.renderer.colorRamp = p.listColorRamps("Yellow to Red")[0]
sym.classBreakValues = ['1.5', '2.0', '3.0', '4.0', '5.0', '6.0']
sym.renderer.breakCount = len(sym.classBreakValues)
# update Break value labels
for brk in sym.renderer.classBreaks:
    brk.label = brk.label.rstrip("0")
lyr.symbology = sym
lyr.transparency = 30

# Adding timestamp
now = datetime.datetime.now()
timeformat = "%d.%m.%Y %H:%M UTC+" + str(time.timezone // -3600)
ts = now.strftime(timeformat)
for t in lyt.listElements("TEXT_ELEMENT"):
    if t.name == "date":
        t.text = "Zeitpunkt: " + ts

# Exporting to jpg
fn_timeformat = "%Y%m%d-%H%M"
filename = "quakes_" + now.strftime(fn_timeformat)
lyt.exportToJPEG(filename)
