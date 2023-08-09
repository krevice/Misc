import pgeocode

def get_lat_long(zip_code):
    nomi = pgeocode.Nominatim("US")
    location = nomi.query_postal_code(zip_code)
    return location.latitude, location.longitude, location.place_name
