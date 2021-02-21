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
# source = alt.topo_feature(data.world_110m.url, 'countries')
source = gpd.read_file("AT_and_neighbors.geojson")

# Layering and configuring the components
background = alt.Chart(source).mark_geoshape(fill='lightgrey', stroke='white')
points = alt.Chart(df_quakes
    ).mark_circle().encode(
        longitude="lon:Q",
        latitude="lat:Q",
        #size=alt.Size("mag_num:Q", title="Magnitude"),
        #size="magmag:Q",
        color="red",
        fillOpacity=0.5
# ).transform_calculate(
#     magmag="int(10*datum.mag)"
).project(
    type='conicConformal',
    center=[8, -3],
    scale=3000,
    rotate=[-1,-49,-14],
    #clipExtent=[[977649, 6281289], [1948091, 5838029]]
).properties(
    width=600, 
    height=400
).configure_view(stroke=None)

m = background + points
m.save("map_at.png", scale_factor=3.0)
