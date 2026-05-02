import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

FUEL_FILE = BASE_DIR / "fuel-prices-for-be-assessment.csv"


def load_fuel_data():

    df = pd.read_csv(FUEL_FILE)

    # Keep required columns only
    df = df[
        [
            "Truckstop Name",
            "Address",
            "City",
            "State",
            "Retail Price"
        ]
    ]

    # Remove rows with missing fuel prices
    df = df.dropna(subset=["Retail Price"])

    return df