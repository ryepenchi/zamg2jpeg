import requests, os

url = "http://geoweb.zamg.ac.at/static/event/lastday.json"
r = requests.get(url)
with open("lastday.json", "wb") as f:
    f.write(r.content)

p = arcpy.mp.ArcGISProject("CURRENT")

arcpy.JSONToFeatures_conversion("lastday.json", os.path.join(p.defaultGeodatabase, "quakes"))


arcpy.management.AddField('quakes', 'mag_new', 'DOUBLE', '', '', '', 'Magnitude', '', '', '')
expression = "!mag!.replace('.',',')"

#vl besser:
# expression = "try2float(!mag!)"
# code_block = """
#     def try2float(mag):
#         if mag == "-":
#             return 0
#         else:
#             return float(mag)
# """
# oder arcpy eigene datamanagement funktionen

# expression für Point size: exp("Magnitude")
# ? Auf Österreich zentrieren, weil NÖ Daten?

try:
    arcpy.management.CalculateField('quakes', 'mag_new', expression, 'PYTHON3')
except:
    pass

m = p.listMaps('Map')[0]

m.addBasemap("Hellgrauer Hintergrund")
m.addDataFromPath(os.path.join(p.defaultGeodatabase, "quakes"))

lyr = m.listLayers('quakes')[0]
sym = lyr.symbology
sym.updateRenderer('GraduatedSymbolsRenderer')
sym.renderer.classificationField = 'mag_new'
sym.renderer.normalizationField = None
sym.renderer.colorRamp = p.listColorRamps("Yellow to Red")[0]
sym.classBreakValues = ['1,5', '2,0', '3,0', '4,0', '5,0', '6,0']
sym.renderer.breakCount = len(sym.classBreakValues)
lyr.symbology = sym
lyr.transparency = 30


# import Layout entweder durch 2tes file oder durch hexacodecheat
p.importDocument("Zamg2JpegExportLayout.pagx")
lyt = p.listLayouts("Zamg2JpegExportLayout")[0]
lyt.exportToJPEG("exportmap.jpg")