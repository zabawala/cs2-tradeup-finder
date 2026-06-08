from load_data import load_prices, load_skins_metadata

import pandas as pd

prices = load_prices()
skins_metadata = load_skins_metadata()

def get_same_rarity_inputs(skins_metadata, rarity):
    possible_pairs = []

    skin_rows = skins_metadata[skins_metadata["rarity"] == rarity]
    skin_names = list(skin_rows["skin_name"])

    for i in range(len(skin_names)):
        for j in range(i + 1, len(skin_names)):
            skin_a = skin_names[i]
            skin_b = skin_names[j]

            possible_pairs.append([skin_a, skin_b])

    return possible_pairs