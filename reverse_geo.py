from pygeocoder import Geocoder
# Convert longitude and latitude to a location
results = Geocoder.reverse_geocode(32.277621,-107.734724)
print results.coordinates
print results.country

print results.street_address

print results.administrative_area_level_1
