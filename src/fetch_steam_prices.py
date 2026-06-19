from pathlib import Path
from load_data import load_skins_metadata

import pandas as pd
import requests
import time
from datetime import datetime, UTC

METADATA_PATH = Path("data/raw/skins_metadata.csv")
OUTPUT_PATH = Path("data/raw/prices.csv")

STEAM_PRICE_URL = "https://steamcommunity.com/market/priceoverview/"

WEAR_BOUNDS = {
    "Factory New": (0.0, 0.07),
    "Minimal Wear": (0.07, 0.15),
    "Field-Tested": (0.15, 0.38),
    "Well-Worn": (0.38, 0.45),
    "Battle-Scarred": (0.45, 1.0),
    }

MAX_REQUESTS_PER_RUN = 100
REQUEST_DELAY_SECONDS = 20
STALE_AFTER_HOURS = 24

def get_valid_wears(min_float, max_float):

    valid_wears = []

    for wear in WEAR_BOUNDS:
        wear_min, wear_max = WEAR_BOUNDS[wear]

        if (min_float < wear_max) and (max_float > wear_min):
            valid_wears.append(wear)

    return valid_wears

def build_market_hash_name(skin_name, wear):
    return f"{skin_name} ({wear})"

def build_price_targets(metadata):
    targets = []
    for index, row in metadata.iterrows():
        skin_name = row["skin_name"]
        min_float = row["min_float"]
        max_float = row["max_float"]

        valid_wears = get_valid_wears(min_float, max_float)

        for wear in valid_wears:
            market_hash_name = build_market_hash_name(skin_name, wear)
            
            targets.append({
                "skin_name": skin_name,
                "wear": wear,
                "market_hash_name": market_hash_name
            })
    
    targets = pd.DataFrame(targets)

    targets = targets.drop_duplicates(
            subset=["skin_name", "wear"]
        ).reset_index(drop=True)

    return targets

def fetch_steam_price(market_hash_name):
    params = {
        "appid": 730,
        "currency": 2,
        "market_hash_name": market_hash_name
    }

    response = requests.get(STEAM_PRICE_URL, params=params)

    status_code = response.status_code

    if status_code == 429:
        return {
            "status_code": status_code, 
            "data": None
        }

    data = response.json()

    return {
        "status_code": status_code, 
        "data": data
    }

    

"""
STRING PARSING FUNCTIONS
"""

def parse_steam_price(price_string):
    if price_string is None:
        return None

    cleaned = price_string.replace("£", "")
    cleaned = cleaned.replace(",", "")
    price = float(cleaned)

    return price

def parse_steam_volume(volume_string):
    if volume_string is None:
        return None

    volume = int(volume_string.replace(",", ""))
    
    return volume

"""
PRICE ROW
"""

def build_price_row(target, data):
    skin_name = target["skin_name"]
    wear = target["wear"]
    market_hash_name = target["market_hash_name"]

    price = parse_steam_price(data.get("lowest_price"))
    volume = parse_steam_volume(data.get("volume"))
    median_price = parse_steam_price(data.get("median_price"))
    success = data.get("success")

    last_checked_utc = datetime.now(UTC).isoformat()

    price_row = {
        "skin_name": skin_name,
        "wear": wear,
        "price": price,
        "volume": volume,
        "median_price": median_price,
        "market_hash_name": market_hash_name,
        "success": success,
        "last_checked_utc": last_checked_utc
    }
    
    return price_row

def load_existing_prices():
    if OUTPUT_PATH.exists():
        prices = pd.read_csv(OUTPUT_PATH)
        return prices
    else:
        return pd.DataFrame()
    
def should_skip_target(target, existing_prices):
    if existing_prices.empty:
        return False

    skin_name = target["skin_name"]
    wear = target["wear"]

    matches = existing_prices[(existing_prices["skin_name"] == skin_name) & (existing_prices["wear"] == wear)]

    if matches.empty:
        print(f'Not cached yet: {target["market_hash_name"]}')
        return False
    
    latest_match = matches.iloc[-1]

#    if pd.isna(latest_match["price"]):
#        return False
    
    last_checked = latest_match["last_checked_utc"]

    if pd.isna(last_checked):
        return False

    last_checked = datetime.fromisoformat(last_checked)
    now = datetime.now(UTC)

    age_hours = (now - last_checked).total_seconds() / 3600

    if age_hours > STALE_AFTER_HOURS:
        print(f'Cached but stale: {target["market_hash_name"]}')
        return False
    
    print(f'Cached and fresh: {target["market_hash_name"]}')
    return True
    





def main():
    metadata = load_skins_metadata()

    industrial_metadata = metadata[metadata["rarity"] == "Industrial Grade"]

    industrial_collections = industrial_metadata["collection"].unique()

    industrial_targets = build_price_targets(industrial_metadata)

    milspec_metadata = metadata[(metadata["rarity"] == "Mil-Spec") & (metadata["collection"].isin(industrial_collections))]

    milspec_targets = build_price_targets(milspec_metadata)

    print(f"Number of industrial metadata rows {len(industrial_metadata)}")
    print()
    print(f"Number of industrial targets: {len(industrial_targets)}")
    print()
    print(f"Number of Mil-Spec targets: {len(milspec_targets)}")
    print()

    existing_prices = load_existing_prices()
    prices = existing_prices.to_dict("records")

    print(f"Existing price rows: {len(existing_prices)}")
    print()

    requests_made = 0
    for index, target in milspec_targets.iterrows():
        if should_skip_target(target, existing_prices):
            print("Skipping already fetched:", target["market_hash_name"])
            continue
        if requests_made >= MAX_REQUESTS_PER_RUN:
            break
        market_hash_name = target["market_hash_name"]
        fetch_result = fetch_steam_price(market_hash_name)
        if fetch_result["status_code"] == 429:
            print("Rate limit reached. Stopping")
            break
        
        data = fetch_result["data"]
        print(data)
        print()
        price_row = build_price_row(target, data)
        print(
            "Fetched:",
            price_row["market_hash_name"],
            "| price:",
            price_row["price"],
            "| volume:",
            price_row["volume"],
            "| median_price:",
            price_row["median_price"]
        )

        prices.append(price_row)

        prices_df = pd.DataFrame(prices)

        prices_df = prices_df.drop_duplicates(
            subset=["skin_name", "wear"],
            keep="last"
        )

        prices_df.to_csv(OUTPUT_PATH, index=False)
        print("Saved progress")

        existing_prices = prices_df

        requests_made += 1

        time.sleep(REQUEST_DELAY_SECONDS)

    print(existing_prices)

main()
