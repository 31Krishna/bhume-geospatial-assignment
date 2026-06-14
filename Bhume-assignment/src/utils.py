from shapely.affinity import translate
from rasterio.features import rasterize
import numpy as np


def alignment_score(
    geom,
    boundary_img,
    transform
):
    mask = rasterize(
        [(geom.boundary.buffer(1.5), 1)],
        out_shape=boundary_img.shape,
        transform=transform,
        fill=0,
        dtype=np.uint8
    )

    overlap = np.sum(
        (mask == 1) &
        (boundary_img == 255)
    )

    total = np.sum(mask == 1)

    return overlap / max(total, 1)


def find_best_shift(
    geom,
    boundary_img,
    transform
):

    original_score = alignment_score(
        geom,
        boundary_img,
        transform
    )

    # Skip search if already decent
    if original_score >= 0.20:
        return (
            0,
            0,
            original_score,
            original_score
        )

    best_score = original_score
    best_dx = 0
    best_dy = 0

    # Reduced search range for speed
    for dx in range(-5, 6):
        for dy in range(-5, 6):

            shifted = translate(
                geom,
                xoff=dx,
                yoff=dy
            )

            score = alignment_score(
                shifted,
                boundary_img,
                transform
            )

            if score > best_score:
                best_score = score
                best_dx = dx
                best_dy = dy

    return (
        best_dx,
        best_dy,
        original_score,
        best_score
    )


def confidence_logic(
    original_score,
    best_score
):

    improvement = (
        best_score -
        original_score
    )

    if improvement >= 0.25:
        return "corrected", 0.95

    elif improvement >= 0.15:
        return "corrected", 0.80

    elif improvement >= 0.08:
        return "corrected", 0.60

    else:
        return "flagged", None