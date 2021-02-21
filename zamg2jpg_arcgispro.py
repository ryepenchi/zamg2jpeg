#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 11:44:33 2020

@author: Carl Löff
@author: Benedikt Müller
@author: Benjamin Reimitz

LV: 2020W 290065-1 Grundlagen der Softwareentwicklung

"""
# imports
import requests, os

# download of daily (last 24h) earthquake data from ZAMG
# alternative file types: csv
# alternative time periods: lastweek, lastmonth
url = "http://geoweb.zamg.ac.at/static/event/lastday.json"
r = requests.get(url)
with open("lastday.json", "wb") as f:
    f.write(r.content)

# priming work with ArcGIS Pro 2.7 Project File
p = arcpy.mp.ArcGISProject("CURRENT")

# arcpy Function converts json to Feature Layer. reason for choosing json over csv
arcpy.JSONToFeatures_conversion("lastday.json", os.path.join(p.defaultGeodatabase, "quakes"))

# Data Field calculations / type conversion for later use in Symbology
arcpy.management.AddField('quakes', 'mag_num', 'DOUBLE', '', '', '', 'Magnitude', '', '', '')

expression = "try2float(!mag!)"
code_block = """
def try2float(mag):
    if mag == "-":
        return 0
    else:
        return float(mag)"""

arcpy.management.CalculateField('quakes', 'mag_num', expression, 'PYTHON3', code_block)

# expression für Point size: exp("Magnitude")
# ? Auf Österreich zentrieren, weil NÖ Daten?

# Defining the Layout
m = p.listMaps('Map')[0]

m.addBasemap("Hellgrauer Hintergrund")
m.addDataFromPath(os.path.join(p.defaultGeodatabase, "quakes"))

lyr = m.listLayers('quakes')[0]
sym = lyr.symbology
sym.updateRenderer('GraduatedSymbolsRenderer')
sym.renderer.classificationField = 'mag_num'
sym.renderer.normalizationField = None
sym.renderer.colorRamp = p.listColorRamps("Yellow to Red")[0]
sym.classBreakValues = ['1,5', '2,0', '3,0', '4,0', '5,0', '6,0']
sym.renderer.breakCount = len(sym.classBreakValues)
lyr.symbology = sym
lyr.transparency = 30


# import predefined Layout
# maybe from external Layouter who is actually good at this
# url = "http://geoweb.zamg.ac.at/static/event/lastday.json"
# r = requests.get(url)
# with open("lastday.json", "wb") as f:
#     f.write(r.content)

p.importDocument("Layout.pagx")
lyt = p.listLayouts("Layout")[0]
lyt.exportToJPEG("exportmap.jpg")