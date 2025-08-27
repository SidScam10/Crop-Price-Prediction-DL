import pandas as pd
import time
import json
import os
import pprint
import glob

from geopy.geocoders import Nominatim


def create_or_update_district_coordinates(csv_file_path, cache_file='district_coordinates.json'):
    # --- Step 1: Load existing coordinates from the cache file ---
    if os.path.exists(cache_file):
        print(f"Loading existing coordinates from '{cache_file}'...")
        with open(cache_file, 'r') as f:
            generated_coordinates = json.load(f)
        print(f"-> Loaded {len(generated_coordinates)} existing entries.")
    else:
        print("No existing coordinate file found. A new one will be created.")
        generated_coordinates = {}

    # Initialize the geolocator
    geolocator = Nominatim(user_agent="district_coordinate_updater_app")

    try:
        # Load the new dataset
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return generated_coordinates, []

    # Get unique districts from the new CSV
    unique_districts_in_data = df['District Name'].unique()
    districts_not_found = []
    new_districts_found = 0

    print("\nChecking for new districts and fetching coordinates...")
    # --- Step 2: Iterate over districts and fetch only if not in cache ---
    for district in unique_districts_in_data:
        # Check if the district is already in our loaded dictionary
        if district in generated_coordinates:
            print(f"-> Skipping '{district}': Already in cache.")
            continue

        # If not in the cache, proceed to fetch it
        try:
            # To improve accuracy, we specify the state and country.
            query = f"{district}, Tamil Nadu, India"
            print(f"Searching for new district: {query}")

            # Fetch the location data
            location = geolocator.geocode(query, timeout=10)

            if location:
                # Add the newly found coordinates to our dictionary
                generated_coordinates[district] = {
                    'lat': location.latitude,
                    'lon': location.longitude
                }
                new_districts_found += 1
                print(f"--> Found and added coordinates for {district}.")
            else:
                # If no location is found, add the district to the not_found list
                print(f"--> Could not find coordinates for {district}.")
                districts_not_found.append(district)

            # Add a delay to be respectful to the geocoding service
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred while processing {district}: {e}")
            districts_not_found.append(district)

    # --- Step 3: Save the updated dictionary back to the cache file ---
    if new_districts_found > 0:
        print(f"\nFound {new_districts_found} new district(s). Saving updated list to '{cache_file}'...")
        with open(cache_file, 'w') as f:
            json.dump(generated_coordinates, f, indent=4)
        print("-> File saved successfully.")
    else:
        print("\nNo new districts were found to add to the cache.")

    return generated_coordinates, districts_not_found

if __name__ == "__main__":
    csv_folder = './3_Cleaned CSVs/'

    csv_files = glob.glob(f"{csv_folder}*.csv")

    # Specify the name of your persistent cache file
    coordinate_cache_file = 'district_coordinates.json'

    for csv_path in csv_files:
        print(f"\nProcessing file: {csv_path}")

        # Call the function to get the combined data
        final_district_data, not_found_list = create_or_update_district_coordinates(
            csv_path,
            cache_file=coordinate_cache_file
        )

        # Print the final, combined dictionary of all found coordinates
        if final_district_data:
            print("\n--- Final Combined District Coordinates ---")
            pprint.pprint(final_district_data)
        else:
            print("\nNo coordinate data was generated.")

        # Print the list of districts that were not found in this specific run
        if not_found_list:
            print("\nCould not find coordinates for the following districts in this run:")
            for district_name in not_found_list:
                print(f"- {district_name}")