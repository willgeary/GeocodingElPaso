
# coding: utf-8

"""
Job description:
I need addresses and cross streets in El Paso, Texas geocoded and matched to their census block groups.

I will provide you with a csv file of addresses and cross streets (no zipcode) that are located in El Paso County, Texas. I need you to return the lat/long of the addresses/cross streets and link the addresses/cross streets to their 2010 U.S. Census block group.

I also require the script you create, along with the readme file.

To the input file (help_recode_address) I would like you to add a variable for the following:
1. latitude (GCS North America)
2. longitude
3. match score
4. 10 digit geoid for census block group

Please make sure the program you create runs on Windows.
"""

### Import libraries
from pandas import read_csv, DataFrame
import requests
from tqdm import tqdm
import pickle
import os
import argparse
from datetime import datetime
import shutil
import geopandas as gpd
from shapely.geometry import Point

## Define functions
def clean_data(df):
    """
    Cleans address csv.
    """
    # Combine address_cross, county and state columns into a full_address column.
    df['full_address'] = df['address_cross'] + ", " + df['county'] + ", " + df['state']
    # Remove '-1/2' from every full address.
    df['full_address'] = df['full_address'].apply(lambda x: str(x).replace("-1/2", ""))
    # Remove specific annotations:
    annotations = ['**VICIOUS K9**', '***EXPOSURE/VICIOUS ANIMAL BITE***', '**INJURED**']
    for i in annotations:
        df['full_address'] = df['full_address'].apply(lambda x: str(x).replace(i, ""))
    # Replace '/' in full_address column with " and ".
    df['full_address'] = df['full_address'].apply(lambda x: str(x).replace("/", " and "))
    return df

def geocode(address, bbox, API_KEY):
    """
    Geocodes an address using Google Maps Geocoding API
    """
    template = "https://maps.googleapis.com/maps/api/geocode/json?address={}&bounds={},{}|{},{}&key={}"
    url = template.format(address, bbox[0], bbox[1], bbox[2], bbox[3], API_KEY)
    response = requests.get(url)
    data = response.json()
    return data

def parse_data(data):
    """
    Parses Google Maps Geocoding API response for
    latitude, longitude, location type and calc's match score
    """
    try:
        lat = data['results'][0]['geometry']['location']['lat']
        lon = data['results'][0]['geometry']['location']['lng']
        location_type = data['results'][0]['geometry']['location_type']
        match_score = get_match_score(location_type)
    except:
        lat = 0
        lon = 0
        match_score = 0
    return (lat, lon, match_score)

def get_match_score(location_type):
    """
    Google Maps Geocoding API v3 does not provide a match score.
    So, I am using this shortcut found here:
    https://stackoverflow.com/questions/7474076/does-the-v3-google-maps-geocoding-api-have-a-field-that-represents-accuracy
    """
    scores = {
        "ROOFTOP": 9,
        "RANGE_INTERPOLATED": 7,
        "GEOMETRIC_CENTER": 6,
        "APPROXIMATE": 4
    }
    if location_type in scores.keys():
        score = scores[location_type]
    else:
        score = 0
    return score


if __name__ == "__main__":
    start_time = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input csv file with addresses")
    args = parser.parse_args()

    # Google Maps Geocoding API Keys (Limit of 2,500 per day per API key)
    API_KEY_1 = "AIzaSyCx2Jn7-R9ryee50s_1yMln-Neq3N3nyvw"
    API_KEY_2 = "AIzaSyAKEgh62VAfGj-GzdS5AjQQHsmjX42InRY"
    API_KEY_3 = "AIzaSyCL_GMWuInCEYLd9ummH_3dumEOoO3RFgE"
    API_KEY_4 = "AIzaSyDdIYRXXsZ8l3E-f73u7EH3qCtfMY4D-fk"
    API_KEY_5 = "AIzaSyA4ZdbUnCd-47styTixrQGxlgoC_Wa0ntw"
    API_KEY_6 = "AIzaSyAGznhayWF9Mnhp6oLDdQGWZxBes2G3wJc"
    API_KEY_7 = "AIzaSyD1-gEJrKTq8IVXDQCz6L9t4J9oRSDPQqo"
    API_KEY_8 = "AIzaSyClcx88xA1VubMvTI40G8zj46yjiYAyEZM"
    API_KEY_9 = "AIzaSyDzYcZSkGF3pAdrN6f5MyaTPQYj1nEr02Y"
    API_KEY_10 = "AIzaSyCqcZkOuLJTIC888_fmQfMq81avIfoDlaM"
    API_KEY_11 = "AIzaSyD4jXA9HCp542Oo19afOJbfgQOCWKIPuwg"
    API_KEY_12 = "AIzaSyDpfCI_nVks137enjcpckb5xb8oag-H9Ew"
    API_KEY_13 = "AIzaSyC-Cheku3EFj1FK3w95IRH3BP9HyptgpYY"
    API_KEY_14 = "AIzaSyDKmEmeefMUPeHFeFAsPvRAv81SQJsWXxk"
    API_KEY_15 = "AIzaSyCoKIdFtCvlJ8uKDrykn4QIbr0OybW88_Y"
    API_KEY_16 = "AIzaSyA3xUzbHtf1h8iUJv80AtvDcNNKiQc7FAU"

    API_KEYS = [API_KEY_1, API_KEY_2, API_KEY_3,  API_KEY_4, API_KEY_5,
                API_KEY_6, API_KEY_7, API_KEY_8, API_KEY_9, API_KEY_10,
                API_KEY_11, API_KEY_12, API_KEY_13, API_KEY_14, API_KEY_15,
                API_KEY_16]

    csvFile = args.input
    df = read_csv(csvFile)
    df = clean_data(df)
    addresses = list(df['full_address'])

    # El Paso bounding box to provide bias for geocoding
    bbox = 31.067051,-107.358398,32.405473,-105.268250

    # Make temporary directory to store serialized files
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Geocode addresses to lat lons and save to temp file
    count = 0
    print("")
    print("Geocoding addresses:")
    for address in tqdm(addresses):
        filename = str(count).zfill(8)
        if os.path.isfile(os.path.join("temp", "{}.pickle".format(filename))):
            pass
        else:
            API_KEY_NUM = int(count / 2400)
            API_KEY = API_KEYS[API_KEY_NUM]
            data = geocode(address, bbox, API_KEY)
            if data['status'] == 'OVER_QUERY_LIMIT':
                print("")
                print("You have exceeded your daily request quota for this API.")
                print("Switching to next available API key.")
                print("")
                API_KEY_NUM += 1
                API_KEY = API_KEYS[API_KEY_NUM]
                data = geocode(address, bbox, API_KEY)
            output = parse_data(data)
            with open(os.path.join("temp", "{}.pickle".format(filename)), 'wb') as f:
                pickle.dump(output, f, protocol=pickle.HIGHEST_PROTOCOL)
        count += 1

    # Load those pickle files to a dataframe
    records = []
    for i in os.listdir(os.path.join("temp")):
        with open(os.path.join("temp", i), "rb") as f:
            record = pickle.load(f)
            records.append(record)
    result = DataFrame.from_records(records)

    # Add the new fields to the dataframe
    df['latitude'] = result[0]
    df['longitude'] = result[1]
    df['match_score'] = result[2]

    # Convert dataframe to geodataframe
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = {'init': 'epsg:4326'}
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

    # Read in texas census block groups
    texas_census_block_groups = "texas_census_block_groups.geojson"
    texas = gpd.read_file(texas_census_block_groups)
    texas = texas.to_crs({'init': 'epsg:4326'})

    # Spatial join points to texas census block groups
    output = gpd.sjoin(gdf, texas, how="left", op='intersects')
    output = output[['counter', 'county', 'state', 'address_cross',
                    'latitude', 'longitude', 'match_score', 'GEOID']]
    output.to_csv("output.csv", index=False)

    # Count number of successes and failures
    print("")
    print(output['latitude'].astype(bool).sum(axis=0), "successes")
    print(len(output) - output['latitude'].astype(bool).sum(axis=0), "failures")

    # Print total time taken
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    hours = int(duration // 3600)
    duration = int(duration - (hours * 3600))
    minutes = int(duration // 60)
    seconds = int(duration - (minutes * 60))
    print("")
    print("Total time taken:",'%s:%s:%s' % (str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2)))
    print("")
