import pandas as pd
import time

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


INPUT_FILE = "fuel-prices-for-be-assessment.csv"
OUTPUT_FILE = "fuel-stations-geocoded.csv"


def geocode_stations():

    df = pd.read_csv(INPUT_FILE)

    # Optional:
    # Remove this line if you want all 8151 rows
    # Keep it if testing only first 300
    # df = df.head(300)

    # Add columns if not present
    if "latitude" not in df.columns:
        df["latitude"] = None

    if "longitude" not in df.columns:
        df["longitude"] = None

    geolocator = Nominatim(user_agent="fuel_station_geocoder")

    for index, row in df.iterrows():

        # Skip already geocoded rows
        if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
            continue

        address = str(row["Address"]).strip()
        city = str(row["City"]).strip()
        state = str(row["State"]).strip()

        full_address = f"{address}, {city}, {state}"

        try:

            # First try full address
            location = geolocator.geocode(
                full_address,
                timeout=10
            )

            # Fallback to city/state
            if not location:

                fallback_address = f"{city}, {state}"

                location = geolocator.geocode(
                    fallback_address,
                    timeout=10
                )

            if location:

                df.at[index, "latitude"] = location.latitude
                df.at[index, "longitude"] = location.longitude

                print(f"Geocoded: {full_address}")

            else:

                print(f"Failed: {full_address}")

        except GeocoderTimedOut:

            print(f"Timeout: {full_address}")

        except Exception as e:

            print(f"Error: {full_address} -> {e}")

        # Save progress every 10 rows
        if index % 10 == 0:

            df.to_csv(OUTPUT_FILE, index=False)

            print("Progress saved...")

        # Avoid rate limiting
        time.sleep(1)

    # Final save
    df.to_csv(OUTPUT_FILE, index=False)

    print("Geocoding completed.")


if __name__ == "__main__":
    geocode_stations()