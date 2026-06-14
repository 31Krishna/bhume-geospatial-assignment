import geopandas as gpd
import rasterio
from shapely.affinity import translate

from utils import (
    find_best_shift,
    confidence_logic
)

plots = gpd.read_file(
    "../data/Vaderbhairav/input.geojson"
)

predictions = []

with rasterio.open(
    "../data/Vaderbhairav/boundaries.tif"
) as src:

    plots = plots.to_crs(src.crs)

    boundary_img = src.read(1)

    for _, row in plots.head(50).iterrows():

        plot_no = str(row["plot_number"])

        geom = row.geometry

        (
            best_dx,
            best_dy,
            original_score,
            best_score
        ) = find_best_shift(
            geom,
            boundary_img,
            src.transform
        )

        status, confidence = confidence_logic(
            original_score,
            best_score
        )

        if status == "corrected":

            new_geom = translate(
                geom,
                xoff=best_dx,
                yoff=best_dy
            )

            note = (
                f"dx={best_dx}, "
                f"dy={best_dy}, "
                f"score {original_score:.3f}"
                f"->{best_score:.3f}"
            )

        else:

            new_geom = geom

            note = (
                f"flagged; "
                f"score {original_score:.3f}"
                f"->{best_score:.3f}"
            )

        predictions.append({
            "plot_number": plot_no,
            "status": status,
            "confidence": confidence,
            "method_note": note,
            "geometry": new_geom
        })

pred_gdf = gpd.GeoDataFrame(
    predictions,
    geometry="geometry",
    crs=plots.crs
)

pred_gdf = pred_gdf.to_crs("EPSG:4326")

pred_gdf.to_file(
    "../predictions.geojson",
    driver="GeoJSON"
)

print(
    "\nDone!"
)

print(
    "Saved: predictions.geojson"
)