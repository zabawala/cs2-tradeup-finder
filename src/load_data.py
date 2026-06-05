from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1] 
# Project starting folder

SKINS_METADATA_PATH = PROJECT_ROOT / "data" / "raw" / "skins_metadata.csv"
PRICES_PATH = PROJECT_ROOT / "data" / "raw" / "prices.csv"
# Path to prices and skins metadata

def check_required_columns(table, required_columns):
    missing_columns = set(required_columns) - set(table.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")
    
# Helper function for loading datas

def load_skins_metadata():
    table = pd.read_csv(SKINS_METADATA_PATH)
    required_columns = [
        "skin_name",
        "collection",
        "rarity",
        "min_float",
        "max_float",
        "stattrak",
    ]
    
    check_required_columns(table, required_columns)

    return table 

def load_prices():
    table = pd.read_csv(PRICES_PATH)
    required_columns = [
        "skin_name",
        "wear",
        "price",
        "volume",
    ]
    
    check_required_columns(table, required_columns)

    return table

def load_combined_table():
    skins_metadata = load_skins_metadata()
    prices = load_prices()

    combined_table = skins_metadata.merge(prices, how="left", on="skin_name")

    return combined_table