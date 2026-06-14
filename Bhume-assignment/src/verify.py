import geopandas as gpd

gdf = gpd.read_file("../predictions.geojson")

print("Total plots:", len(gdf))

print("\nColumns:")
print(gdf.columns)

print("\nStatus counts:")
print(gdf["status"].value_counts())

print("\nFirst 5 rows:")
print(
    gdf[
        ["plot_number",
         "status",
         "confidence"]
    ].head()
)