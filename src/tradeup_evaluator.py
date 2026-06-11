from load_data import load_prices, load_skins_metadata

import pandas as pd

skins_metadata = load_skins_metadata()
prices = load_prices()

example_recipe = [
    "MAC-10 | Silver",
    "Nova | Candy Apple"
]
    
# Helper function to check whether recipe has exactly 10 skins

def create_price_lookup(prices):
    required_columns = ["skin_name", "wear", "price"]

    for column in required_columns:
        if column not in prices.columns:
            raise ValueError(f"Missing required column in prices: {column}")

    duplicate_prices = prices.duplicated(subset=["skin_name", "wear"], keep=False)

    if duplicate_prices.any():
        duplicates = prices[duplicate_prices][["skin_name", "wear"]]
        raise ValueError(f"Duplicate price rows found:\n{duplicates}")

    price_lookup = prices.set_index(["skin_name", "wear"])["price"].to_dict()

    return price_lookup

def calculate_adjusted_float(actual_float, min_float, max_float):
    adjusted_float = (actual_float - min_float)/(max_float - min_float)

    return adjusted_float

def get_adjusted_breaking_points(row):
    max_float = row["max_float"]
    min_float = row["min_float"]

    float_breaking_points = [0.07, 0.15, 0.38, 0.45]

    adjusted_breakpoints = []

    for boundary in float_breaking_points:
        if min_float < boundary < max_float:
            adjusted = calculate_adjusted_float(boundary, min_float, max_float)
            adjusted_breakpoints.append(adjusted)

    return adjusted_breakpoints

def get_adjusted_table(skins_metadata):
    adjusted_table = skins_metadata.copy()
    adjusted_table["adjusted_breakpoints"] = adjusted_table.apply(get_adjusted_breaking_points, axis=1)

    return adjusted_table

def get_input_table(recipe, adjusted_table):
    result = adjusted_table[adjusted_table["skin_name"].isin(recipe)]

    return result

def check_input_skins_exist(recipe, adjusted_table):
    recipe_skins = set(recipe)
    found_skins = set(adjusted_table["skin_name"].unique())

    missing_skins = recipe_skins - found_skins

    if missing_skins:
        raise ValueError(f"Recipe skins not found in data: {missing_skins}")

def get_input_rarity(input_table):
    unique_rarities = input_table["rarity"].unique()

    if len(unique_rarities) != 1:
        raise ValueError("All 10 skins must have the same rarity")
    
    input_rarity = unique_rarities[0]
    return input_rarity

def get_output_rarity(input_rarity):

    rarity_outputs = {
        "Consumer Grade": "Industrial Grade",
        "Industrial Grade": "Mil-Spec",
        "Mil-Spec": "Restricted",
        "Restricted": "Classified",
        "Classified": "Covert"
    }
    
    if input_rarity not in rarity_outputs:
        raise ValueError(f"No output rarity exists for input rarity: {input_rarity}")
    
    output_rarity = rarity_outputs[input_rarity]
    return output_rarity

# Another helper function to check whether recipe has same rarity and gives the output rarity of the recipe


def get_possible_outputs(input_table, adjusted_table):
    collections = set(input_table["collection"])
    collection_skins = adjusted_table[adjusted_table["collection"].isin(collections)]
    # Creates a table with all the skins of all the collections in the recipe
    input_rarity = get_input_rarity(input_table)

    output_rarity = get_output_rarity(input_rarity)
    possible_outputs = collection_skins[collection_skins["rarity"] == output_rarity]
    # Filters the previous table by the target rarity

    return possible_outputs

def get_unique_adjusted_breakpoints(possible_outputs):
    all_breakpoints = []

    for breakpoints in possible_outputs["adjusted_breakpoints"]:
        for breakpoint in breakpoints:
            all_breakpoints.append(breakpoint)

    unique_breakpoints = sorted(set(all_breakpoints))

    return unique_breakpoints

"""
Calculating Profitability
"""

def classify_wear(float_value):
    if float_value < 0.07:
        return "Factory New"
    elif float_value < 0.15:
        return "Minimal Wear"
    elif float_value < 0.38:
        return "Field-Tested"
    elif float_value < 0.45:
        return "Well-Worn"
    else:
        return "Battle-Scarred"
    

def get_actual_float_from_adjusted(adjusted_float, min_float, max_float):
    actual_float = (adjusted_float * (max_float - min_float)) + min_float

    return actual_float

def get_input_float_and_wear(breakpoint, input_table):
    input_with_float_and_wear = input_table.drop(columns=["adjusted_breakpoints"]).copy()

    target_adjusted_float = breakpoint - 0.000001

    input_floats = []

    for index, row in input_with_float_and_wear.iterrows():
        min_float = row["min_float"]
        max_float = row["max_float"]

        actual_float = get_actual_float_from_adjusted(target_adjusted_float, min_float, max_float)

        input_floats.append(actual_float)

    input_with_float_and_wear["input_float"] = input_floats

    input_with_float_and_wear["wear"] = input_with_float_and_wear["input_float"].apply(classify_wear)

    return input_with_float_and_wear


def get_output_float_and_wear(breakpoint, possible_outputs):
    output_with_float_and_wear = possible_outputs.copy()

    target_adjusted_float = breakpoint - 0.000001

    output_floats = []

    for index, row in possible_outputs.iterrows():
        min_float = row["min_float"]
        max_float = row["max_float"]

        actual_float = get_actual_float_from_adjusted(target_adjusted_float, min_float, max_float)

        output_floats.append(actual_float)

    output_with_float_and_wear["output_float"] = output_floats

    output_with_float_and_wear["wear"] = output_with_float_and_wear["output_float"].apply(classify_wear)

    return output_with_float_and_wear

def get_price(prices, skin_name, wear):
    key = (skin_name, wear)

    if key not in prices:
        raise ValueError(f"Missing price for {skin_name} in {wear}")

    return prices[key]

# Helper function for prices

def get_input_prices(input_with_float_and_wear, prices):
    input_with_prices = input_with_float_and_wear.copy()

    input_with_prices["price"] = input_with_prices.apply(
        lambda row: get_price(prices, row["skin_name"], row["wear"]),
        axis=1
    )
    
    return input_with_prices

def get_output_prices(output_with_float_and_wear, prices):
    output_with_prices = output_with_float_and_wear.copy()

    output_with_prices["price"] = output_with_prices.apply(
        lambda row: get_price(prices, row["skin_name"], row["wear"]),
        axis=1
    )
    
    return output_with_prices

def compute_input_cost(recipe, k, input_with_prices):
    recipe_quantities = {
        recipe[0]: k,
        recipe[1]: 10 - k,
    }

    input_cost = 0.0

    for index, row in input_with_prices.iterrows():
        skin_name = row["skin_name"]
        price = row["price"]
        quantity = recipe_quantities[skin_name]

        input_cost += price * quantity

    return input_cost

def get_collection_expected_values(output_with_prices):
    collection_expected_values = (
        output_with_prices
        .groupby("collection")["price"]
        .mean()
        .to_dict()
    )

    return collection_expected_values

def compute_expected_output_from_collections(recipe, k, input_table, collection_expected_values):
    recipe_quantities = {
        recipe[0]: k,
        recipe[1]: 10 - k
    }

    expected_output = 0.0

    for skin_name, quantity in recipe_quantities.items():
        skin_row = input_table[input_table["skin_name"] == skin_name]
        collection = skin_row["collection"].iloc[0]

        collection_expected_value = collection_expected_values[collection]

        expected_output += (quantity / 10) * collection_expected_value

    return expected_output

def compute_expected_profit(expected_output, input_cost):
    return expected_output - input_cost

def compute_roi(expected_profit, input_cost):
    return expected_profit / input_cost


def get_wear_bounds(wear):
    wear_bounds = {
        "Factory New": (0.00, 0.07),
        "Minimal Wear": (0.07, 0.15),
        "Field-Tested": (0.15, 0.38),
        "Well-Worn": (0.38, 0.45),
        "Battle-Scarred": (0.45, 1.00)
    }

    if wear not in wear_bounds:
        raise ValueError(f"Unknown wear: {wear}")
    
    return wear_bounds[wear]

# Helper function for wastage


def compute_row_wastage(row):
    input_float = row["input_float"]
    wear = row["wear"]

    wear_min, wear_max = get_wear_bounds(wear)
    
    lower_bound = max(wear_min, row["min_float"])
    upper_bound = min(wear_max, row["max_float"])

    range = upper_bound - lower_bound

    if range <= 0:
        raise ValueError("Invalid wear band for input skin")
    
    wastage = (upper_bound - input_float) / range

    return wastage

def compute_input_wastage(recipe, k, input_with_prices):
    recipe_quantities = {
        recipe[0]: k,
        recipe[1]: 10 - k
    }

    total_quantity = 0
    total_weighted_wastage = 0.0

    for index, row in input_with_prices.iterrows():
        skin_name = row["skin_name"]
        quantity = recipe_quantities[skin_name]

        row_wastage = compute_row_wastage(row)

        total_weighted_wastage += row_wastage * quantity
        total_quantity += quantity

    return total_weighted_wastage / total_quantity

def compute_tradeup_score(roi, wastage):
    return roi * (1 - wastage)



"""
WRAPPER FUNCTION FOR 1 CANDIDATE
"""

def evaluate_candidate(recipe, k, breakpoint, input_with_prices, expected_output):

    input_cost = compute_input_cost(
        recipe,
        k,
        input_with_prices
    )

    expected_profit = compute_expected_profit(
        expected_output,
        input_cost
    )

    roi = compute_roi(
        expected_profit,
        input_cost
    )

    wastage = compute_input_wastage(
        recipe,
        k,
        input_with_prices
    )

    score = compute_tradeup_score(
        roi,
        wastage
    )

    result = {
        "skin_a": recipe[0],
        "skin_b": recipe[1],
        "k": k,
        "ratio": f"{k}:{10 - k}",
        "breakpoint": breakpoint,
        "target_adjusted_float": breakpoint - 0.000001,
        "input_cost": input_cost,
        "expected_output": expected_output,
        "expected_profit": expected_profit,
        "roi": roi,
        "wastage": wastage,
        "score": score
    }

    return result