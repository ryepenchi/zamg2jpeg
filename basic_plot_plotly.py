import plotly.express as px
import geopandas as gpd

df_quakes = gpd.read_file("lastday.json")
df_quakes = df_quakes[df_quakes["mag"]!="-"]
df_quakes["mag_num"] = df_quakes["mag"].astype(float)
df_quakes = df_quakes[df_quakes.mag_num > 0]

px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_geo(df_quakes,
                    lat=df_quakes.lat,
                    lon=df_quakes.lon,
                    size=df_quakes.mag_num
                    )
fig.show()
