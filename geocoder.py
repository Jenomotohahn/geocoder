import requests
import csv
import time

# google API key
GOOGLE_API_KEY = "blah blah blah"


# function to retrieve lat and long from Google geocode API
def extract_lat_long_via_address(address_zip):
    api_key = GOOGLE_API_KEY
    baseurl = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{baseurl}?address={address_zip}&key={api_key}"
    r = requests.get(endpoint)
    print(r.status_code)
    lat, lng = None, None
    if r.status_code not in range(200, 299):
        print(f"{address_zip} not found")
        coordinate = [lat, lng]
        return coordinate

    try:
        results = r.json()["results"][0]
        lat = results["geometry"]["location"]["lat"]
        lng = results["geometry"]["location"]["lng"]
        coordinates = [lat, lng]
    except:
        pass
    return coordinates


with open("python file.csv") as f:
    with open("newfile.csv", "w", newline="") as newcsv:
        reader = csv.DictReader(f)
        fieldnames = [
            "ID",
            "Description",
            "Address Line 1",
            "City",
            "State",
            "Postal Code",
            "latitude",
            "longitude",
        ]
        writer = csv.DictWriter(newcsv, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            newaddress = f"{row['Address Line 1']} {row['City']} {row['State']} {row['Postal Code']}"
            result = extract_lat_long_via_address(newaddress)
            row["latitude"] = result[0]
            row["longitude"] = result[1]
            writer.writerow(row)
