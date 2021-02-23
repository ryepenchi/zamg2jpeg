#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 11:44:33 2020

LV: 2020W 290065-1 Grundlagen der Softwareentwicklung
"""
# imports
import arcpy
import requests, os, datetime

# download of daily (last 24h) earthquake data from ZAMG
# alternative file types: csv
# alternative time periods: lastweek, lastmonth
url = "http://geoweb.zamg.ac.at/static/event/lastday.json"
r = requests.get(url)
with open("lastday.json", "wb") as f:
    f.write(r.content)

# priming work with ArcGIS Pro 2.7 Project File
p = arcpy.mp.ArcGISProject("zamg2jpeg.aprx")

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

# expression für Point size: exp("Magnitude")
# ? Auf Österreich zentrieren, weil NÖ Daten?

# Importing Layout first to work around broken Data Source Path
# url = "https://raw.githubusercontent.com/ryepenchi/zamg2jpeg/main/Layout.pagx"
# r = requests.get(url)
# with open("Layout.pagx", "wb") as f:
#     f.write(r.content)
p.importDocument(os.path.join(p.homeFolder, "Layout.pagx"))
lyt = p.listLayouts("Layout")[0]

# Defining the Layer
# m = p.listMaps('Map')[0]

# m.addBasemap("Hellgrauer Hintergrund")
# m.addDataFromPath(os.path.join(p.defaultGeodatabase, "quakes"))
lyt.listElements("MAPFRAME_ELEMENT")[0].map.addDataFromPath(os.path.join(p.defaultGeodatabase, "quakes"))

#lyr = m.listLayers('quakes')[0]
lyr = lyt.listElements("MAPFRAME_ELEMENT")[0].map.listLayers("quakes")[0]

sym = lyr.symbology
sym.updateRenderer('GraduatedSymbolsRenderer')
sym.renderer.classificationField = 'Magnitude'
sym.renderer.normalizationField = None
sym.renderer.colorRamp = p.listColorRamps("Yellow to Red")[0]
sym.classBreakValues = ['1.5', '2.0', '3.0', '4.0', '5.0', '6.0']
sym.renderer.breakCount = len(sym.classBreakValues)
#update Break value labels
for brk in sym.renderer.classBreaks:
    brk.label = brk.label.rstrip("0")
lyr.symbology = sym
lyr.transparency = 30

# Making the Legend
timeformat = "%d.%m.%Y"
now = datetime.datetime.now()
# yesterday = now - datetime.timedelta(days = 1)
now = now.strftime(timeformat)
# yesterday = yesterday.strftime(timeformat)

lyt.listElements("LEGEND_ELEMENT")[0].showTitle = True
lyt.listElements("LEGEND_ELEMENT")[0].title = now

# Exporting to jpg

lyt.exportToJPEG("exportmap.jpg")