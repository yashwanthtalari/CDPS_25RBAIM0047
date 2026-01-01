import rasterio

dem = rasterio.open("data/dem.tif")
transform = dem.transform
dem_data = dem.read(1)

def get_elevation(lat, lon):
    col, row = ~transform * (lon, lat)
    row = int(row)
    col = int(col)

    # Boundaries
    row = max(0, min(row, dem_data.shape[0] - 1))
    col = max(0, min(col, dem_data.shape[1] - 1))

    return float(dem_data[row, col])
