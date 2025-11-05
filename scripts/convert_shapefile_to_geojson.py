import geopandas as gpd
import json

# Read the shapefile
shapefile_path = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\ARRealignment\Data\tl_2020_05_county20\tl_2020_05_county20.shp"
gdf = gpd.read_file(shapefile_path)

# Convert to GeoJSON (WGS84 - EPSG:4326 for web mapping)
gdf_wgs84 = gdf.to_crs("EPSG:4326")

# Save as GeoJSON
output_path = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\ARRealignment\Data\tl_2020_05_county20.geojson"
gdf_wgs84.to_file(output_path, driver='GeoJSON')

print(f"GeoJSON created successfully at: {output_path}")
print(f"Number of counties: {len(gdf_wgs84)}")
print(f"\nColumn names in shapefile:")
print(gdf_wgs84.columns.tolist())
print(f"\nFirst county sample:")
print(gdf_wgs84.head(1))
