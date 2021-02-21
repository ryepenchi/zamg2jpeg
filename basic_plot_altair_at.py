import altair as alt
from vega_datasets import data
import geopandas as gpd

#bug hunting
import numpy as np
import pandas as pd

df_quakes = gpd.read_file("lastday.json")
df_quakes = df_quakes[df_quakes["mag"]!="-"]
df_quakes["mag_num"] = df_quakes["mag"].astype(float)
df_quakes = df_quakes[df_quakes.mag_num > 0]
df_quakes["mag_int"] = df_quakes["mag_num"].astype("int32", errors="ignore")

#bug hunting
r = np.random.randint(0,100,size=878)
df_quakes["test"] = r
print(df_quakes.dtypes)
print(df_quakes["mag_int"])
input("Hold....")
# Data generators for the background
sphere = alt.sphere()
graticule = alt.graticule()

# Source of land data
# source = alt.topo_feature(data.world_110m.url, 'countries')
source = gpd.read_file("AT_and_neighbors.geojson")

# Layering and configuring the components
m = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue'),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
    alt.Chart(source).mark_geoshape(fill='lightgrey', stroke='white'),
    alt.Chart(df_quakes).mark_circle(
        size="mag_int:Q",
        color="red",
        fillOpacity=0.5
    ).encode(
        longitude="lon:Q",
        latitude="lat:Q"
    )
).project(
    type='conicConformal',
    center=[8, -3],
    scale=3000,
    rotate=[-1,-49,-14],
    #clipExtent=[[977649, 6281289], [1948091, 5838029]]
).properties(width=600, height=400).configure_view(stroke=None)

m.save("map_at.png", scale_factor=3.0)
