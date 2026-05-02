import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

FUEL_FILE = BASE_DIR / "fuel-stations-geocoded.csv"


def load_stations():

    df = pd.read_csv(FUEL_FILE)

    # Remove invalid coordinates
    df = df.dropna(subset=["latitude", "longitude"])

    return df