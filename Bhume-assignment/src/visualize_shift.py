import geopandas as gpd
import rasterio
from rasterio.windows import from_bounds
from rasterio.features import rasterize
from shapely.affinity import translate
import numpy as np
import matplotlib.pyplot as plt

PLOT_NUMBER = "1"

# Load plots
plots = gpd.read_file("../data/Vaderbhairav/input.geojson")

plot = plots[
    plots["plot_number"].astype(str) == PLOT_NUMBER
]

with rasterio.open("../data/Vaderbhairav/boundaries.tif") as src:

    plot = plot.to_crs(src.crs)

    original_geom = plot.geometry.iloc[0]

    # Best shift found from shift_search.py
    shifted_geom = translate(
        original_geom,
        xoff=17,
        yoff=6
    )

    minx, miny, maxx, maxy = plot.total_bounds

    pad = 100

    window = from_bounds(
        minx - pad,
        miny - pad,
        maxx + pad,
        maxy + pad,
        transform=src.transform
    )

    boundary_crop = src.read(1, window=window)

    crop_transform = src.window_transform(window)

    # Original plot mask
    original_mask = rasterize(
        [(original_geom.boundary.buffer(1.5), 1)],
        out_shape=boundary_crop.shape,
        transform=crop_transform,
        fill=0,
        dtype=np.uint8
    )

    # Shifted plot mask
    shifted_mask = rasterize(
        [(shifted_geom.boundary.buffer(1.5), 1)],
        out_shape=boundary_crop.shape,
        transform=crop_transform,
        fill=0,
        dtype=np.uint8
    )

    plt.figure(figsize=(8,8))

    # White = detected boundaries
    plt.imshow(boundary_crop, cmap="gray")

    # Red = original
    plt.imshow(
        np.ma.masked_where(original_mask == 0, original_mask),
        cmap="Reds",
        alpha=0.7
    )

    # Green = shifted
    plt.imshow(
        np.ma.masked_where(shifted_mask == 0, shifted_mask),
        cmap="Greens",
        alpha=0.7
    )

    plt.title(
        "White=Boundaries  Red=Original  Green=Shifted"
    )

    plt.axis("off")
    plt.show()