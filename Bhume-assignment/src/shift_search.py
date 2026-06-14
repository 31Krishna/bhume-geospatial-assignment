import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from shapely.affinity import translate
import numpy as np

PLOT_NUMBER = "1"

plots = gpd.read_file("../data/Vaderbhairav/input.geojson")

plot = plots[
    plots["plot_number"].astype(str) == PLOT_NUMBER
]

with rasterio.open("../data/Vaderbhairav/boundaries.tif") as src:

    plot = plot.to_crs(src.crs)

    boundary_img = src.read(1)

    best_score = -1
    best_dx = 0
    best_dy = 0

    # Search +-20 meters
    for dx in range(-20, 21):
        for dy in range(-20, 21):

            shifted_geom = translate(
                plot.geometry.iloc[0],
                xoff=dx,
                yoff=dy
            )

            mask = rasterize(
                [(shifted_geom.boundary.buffer(1.5), 1)],
                out_shape=boundary_img.shape,
                transform=src.transform,
                fill=0,
                dtype=np.uint8
            )

            overlap = np.sum(
                (mask == 1) &
                (boundary_img == 255)
            )

            total = np.sum(mask == 1)

            score = overlap / max(total, 1)

            if score > best_score:
                best_score = score
                best_dx = dx
                best_dy = dy

    print("\n===== RESULT =====")
    print("Plot:", PLOT_NUMBER)
    print("Best DX:", best_dx)
    print("Best DY:", best_dy)
    print("Best Score:", round(best_score, 4))