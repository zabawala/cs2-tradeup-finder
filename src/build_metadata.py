import pandas as pd
import requests
from pathlib import Path


SKINS_URL = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"

OUTPUT_PATH = Path("data/raw/skins_metadata.csv")

INVALID_CATEGORIES = {
    "Knives",
    "Gloves",
    "Equipment",
}

VALID_RARITIES = {
    "Consumer Grade",
    "Industrial Grade",
    "Mil-Spec Grade",
    "Restricted",
    "Classified",
    "Covert",
}

RARITY_NORMALISATION = {
    "Mil-Spec Grade": "Mil-Spec",
}


def fetch_skins_json():
    response = requests.get(SKINS_URL)
    response.raise_for_status()
    return response.json()


def normalise_rarity(rarity):
    return RARITY_NORMALISATION.get(rarity, rarity)


def get_source_groups(skin):
    collections = skin.get("collections", [])

    if collections:
        return collections

    crates = skin.get("crates", [])

    if crates:
        return crates

    return []


def is_valid_tradeup_skin(skin):
    category = skin.get("category", {}).get("name")
    rarity = skin.get("rarity", {}).get("name")
    source_groups = get_source_groups(skin)

    if category in INVALID_CATEGORIES:
        return False

    if rarity not in VALID_RARITIES:
        return False

    if not source_groups:
        return False

    if skin.get("min_float") is None:
        return False

    if skin.get("max_float") is None:
        return False

    return True


def convert_skin_to_metadata_rows(skin):
    rows = []

    skin_name = skin["name"]
    weapon = skin["weapon"]["name"]
    category = skin["category"]["name"]
    rarity = normalise_rarity(skin["rarity"]["name"])
    min_float = skin["min_float"]
    max_float = skin["max_float"]

    # These mean availability, not necessarily that this row is StatTrak/Souvenir.
    stattrak_available = skin.get("stattrak", False)
    souvenir_available = skin.get("souvenir", False)

    source_groups = get_source_groups(skin)

    for group in source_groups:
        row = {
            "skin_name": skin_name,
            "weapon": weapon,
            "category": category,
            "collection": group["name"],
            "rarity": rarity,
            "min_float": min_float,
            "max_float": max_float,

            # For now, we are building normal non-StatTrak tradeup metadata.
            "stattrak": False,
            "souvenir": False,

            # Useful info to keep for later.
            "stattrak_available": stattrak_available,
            "souvenir_available": souvenir_available,
        }

        rows.append(row)

    return rows


def build_metadata_table(skins):
    metadata_rows = []

    for skin in skins:
        if not is_valid_tradeup_skin(skin):
            continue

        rows = convert_skin_to_metadata_rows(skin)
        metadata_rows.extend(rows)

    metadata = pd.DataFrame(metadata_rows)

    if metadata.empty:
        raise ValueError("No valid skins found. Check filtering logic.")

    metadata = metadata.drop_duplicates(
        subset=["skin_name", "collection", "rarity", "stattrak", "souvenir"]
    )

    metadata = metadata.sort_values(
        by=["rarity", "collection", "skin_name"]
    ).reset_index(drop=True)

    return metadata


def main():
    skins = fetch_skins_json()

    metadata = build_metadata_table(skins)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("Number of metadata rows:", len(metadata))
    print(metadata.head(20))

    print()
    print("Rarity counts:")
    print(metadata["rarity"].value_counts())

    print()
    print("Category counts:")
    print(metadata["category"].value_counts())

    metadata.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved metadata to {OUTPUT_PATH}")


main()