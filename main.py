import pyproj

def lat_lon_to_utm(lat, lon):
    # Create a UTM projection based on the longitude
    utm_proj = pyproj.Proj(proj='utm', zone=int((lon + 180) / 6) + 1, ellps='WGS84')
    easting, northing = utm_proj(lon, lat)
    return easting, northing

def main():
    # Coordinates for Los Angeles and New York
    lat_la, lon_la = 34.0522, -118.2437  # Los Angeles, CA
    lat_ny, lon_ny = 40.7128, -74.0060   # New York, NY

    # Convert to UTM
    easting_la, northing_la = lat_lon_to_utm(lat_la, lon_la)
    easting_ny, northing_ny = lat_lon_to_utm(lat_ny, lon_ny)

    # Calculate differences
    easting_diff = easting_la - easting_ny
    northing_diff = northing_la - northing_ny

    print(f"Difference in Easting (LA - NY): {easting_diff:.2f} meters")
    print(f"Difference in Northing (LA - NY): {northing_diff:.2f} meters")

if __name__ == "__main__":
    main()

