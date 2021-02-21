import altair as alt
from vega_datasets import data
import geopandas as gpd

df_quakes = gpd.read_file("lastday.json")
df_quakes = df_quakes[df_quakes["mag"]!="-"]
df_quakes["mag_num"] = df_quakes["mag"].astype(float)
df_quakes = df_quakes[df_quakes.mag_num > 0]

# Data generators for the background
sphere = alt.sphere()
graticule = alt.graticule()

# Source of land data
source = alt.topo_feature(data.world_110m.url, 'countries')

# Layering and configuring the components
m = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue'),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
    alt.Chart(source).mark_geoshape(fill='lightgrey', stroke='black'),
    alt.Chart(df_quakes).mark_circle(
        size=1,
        color="red"
    ).encode(
        longitude="lon:Q",
        latitude="lat:Q"
    )
).project(
    'naturalEarth1'
).properties(width=600, height=400).configure_view(stroke=None)

m.save("map.png", scale_factor=3.0)
