import geopandas as gpd

gdf = gpd.read_file("../predictions.geojson")

print("\n===== SUMMARY =====")
print("Total plots:", len(gdf))

print("\nCorrected:")
print((gdf["status"] == "corrected").sum())

print("\nFlagged:")
print((gdf["status"] == "flagged").sum())

print("\nAverage confidence:")
print(
    gdf["confidence"]
    .dropna()
    .mean()
)