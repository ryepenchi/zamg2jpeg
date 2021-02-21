import geopandas as gpd
import geoplot
import matplotlib.pyplot as plt

df_quakes = gpd.read_file("lastday.json")
df_quakes = df_quakes[df_quakes["mag"]!="-"]
df_quakes["mag_num"] = df_quakes["mag"].astype(float)
df_quakes = df_quakes[df_quakes.mag_num > 0]


world = gpd.read_file(
    gpd.datasets.get_path('naturalearth_lowres')
)

ax = geoplot.polyplot(world, figsize=(12, 6))
geoplot.pointplot(df_quakes, ax=ax, color="red", scale="mag_num", limits=(0.5,1.5))

plt.show()
