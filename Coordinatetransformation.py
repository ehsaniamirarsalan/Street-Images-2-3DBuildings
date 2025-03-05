import pyproj

def convert_wgs84_to_utm(latitude, longitude):
    # Define WGS84 (EPSG:4326) and UTM EPSG:25832 projections
    wgs84 = pyproj.Proj(init='epsg:4326')
    utm = pyproj.Proj(init='epsg:25832')

    # Transform coordinates
    utm_x, utm_y = pyproj.transform(wgs84, utm, longitude, latitude)
    
    return utm_x, utm_y

latitude = 52.5200
longitude = 13.4050
utm_x, utm_y = convert_wgs84_to_utm(latitude, longitude)
print("UTM X:", utm_x)
print("UTM Y:", utm_y)