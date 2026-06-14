# BhuMe AI Geospatial Assignment

## Overview

This project detects and corrects misaligned agricultural plot boundaries using rasterized field boundaries.

The solution:

1. Loads plot polygons from `input.geojson`
2. Converts geometries to raster CRS
3. Computes alignment scores using overlap with detected boundaries
4. Searches nearby shifts
5. Applies corrections when confidence is sufficient
6. Flags uncertain cases for manual review

---

## Method

### Alignment Score

A plot boundary is rasterized and compared against the boundary raster.

Score:

alignment = overlap_pixels / total_boundary_pixels

### Shift Search

For every plot:

- Search nearby dx, dy shifts
- Compute alignment score
- Select best shift

### Confidence Logic

| Improvement | Confidence |
|------------|------------|
| >= 0.25 | 0.95 |
| >= 0.15 | 0.80 |
| >= 0.08 | 0.60 |
| otherwise | Flagged |

---

## Output

The generated file:

predictions.geojson

contains:

- plot_number
- status
- confidence
- method_note
- geometry

---

## Results

Example run:

- Total plots processed: 50
- Corrected: 14
- Flagged: 36
- Average confidence: 0.68

---

## Run

```bash
pip install -r requirements.txt

python predict.py

python verify.py

python summary.py
```
