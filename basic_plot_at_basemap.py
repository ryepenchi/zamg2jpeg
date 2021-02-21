import geopandas as gpd
import geoplot
import matplotlib.pyplot as plt
import contextily as ctx

df_quakes = gpd.read_file("lastday.json")
df_quakes = df_quakes[df_quakes["mag"]!="-"]
df_quakes["mag_num"] = df_quakes["mag"].astype(float)
df_quakes = df_quakes[df_quakes.mag_num > 0]


extent = (950000, 2000000, 5800000, 6300000)
df_quakes.to_crs(epsg=3857)
ax = geoplot.pointplot(df_quakes, color="red", scale="mag_num", limits=(0.5,1.5))
ax.axis(extent)
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, zoom=6)
plt.show()

#source=ctx.providers.BasemapAT.grau
