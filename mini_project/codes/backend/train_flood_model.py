import pandas as pd
import rasterio
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

print("Loading data...")

# Load labels
labels = pd.read_csv("data/labels.csv")

# Load rainfall (no coordinates)
rain = pd.read_csv("data/rainfall.csv")
avg_rainfall = rain["rainfall_mm"].mean()
labels["rainfall"] = avg_rainfall

# Load DEM once
print("Loading DEM into memory (this may take a few seconds)...")
with rasterio.open("data/dem.tif") as src:
    dem_data = src.read(1)            # Full raster stored in RAM
    transform = src.transform         # Affine transform for indexing

print("DEM loaded. Sampling elevations...")

# Vectorized coordinate-to-row/col conversion
lon = labels["x"].values
lat = labels["y"].values

# Convert coordinates → pixel indices
inv_transform = ~transform
cols, rows = inv_transform * (lon, lat)

# Ensure indices are valid integers
rows = rows.astype(int)
cols = cols.astype(int)

# Clip rows & cols to raster bounds (avoid index errors)
rows = np.clip(rows, 0, dem_data.shape[0] - 1)
cols = np.clip(cols, 0, dem_data.shape[1] - 1)

# Extract elevation values in one vectorized operation
labels["elevation"] = dem_data[rows, cols]

print("Elevation sampling completed.")

# ML Dataset
X = labels[["elevation", "rainfall"]]
y = labels["cat"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training model...")
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

print("\nMODEL REPORT:")
print(classification_report(y_test, model.predict(X_test)))

# Save trained model
joblib.dump(model, "models/flood_model.pkl")

print("\nFlood model saved → models/flood_model.pkl")
