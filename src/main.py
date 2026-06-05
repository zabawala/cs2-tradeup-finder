from load_data import load_prices, load_skins_metadata, load_combined_table

skins_metadata = load_skins_metadata()
prices = load_prices()
combined_table = load_combined_table()

print(f"Skins MetaData:")
print(f"{skins_metadata}")

print(f"Prices:")
print(f"{prices}")

print(f"Full Table")
print(f"{combined_table}")

example_recipe = {
    "MAC-10 | Silver":  7,
    "Nova | Candy Apple": 3
}

def get_input_table(recipe, combined_table):
    result = combined_table[combined_table["skin_name"].isin(recipe.keys())]
    return result

"""
Recipe Validation
"""

def check_recipe_quantity(recipe):
    total_quantity = sum(recipe.values())

    if total_quantity != 10:
        raise ValueError("Recipe must contain exactly 10 skins")
    
# Helper function to check whether recipe has exactly 10 skins

def get_input_rarity(input_table):
    unique_rarities = input_table["rarity"].unique()

    if len(unique_rarities) != 1:
        raise ValueError("All 10 skins must have the same rarity")
    
    input_rarity = unique_rarities[0]
    return input_rarity

def check_input_skins_exist(recipe, input_table):
    recipe_skins = set(recipe.keys())
    found_skins = set(input_table["skin_name"].unique())

    missing_skins = recipe_skins - found_skins

    if missing_skins:
        raise ValueError(f"Recipe skins not found in data: {missing_skins}")

"""
Tradeup Mechanics
"""

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


def get_possible_outputs(input_table, combined_table):
    collections = set(input_table["collection"])
    collection_skins = combined_table[combined_table["collection"].isin(collections)]
    # Creates a table with all the skins of all the collections in the recipe
    input_rarity = get_input_rarity(input_table)

    output_rarity = get_output_rarity(input_rarity)
    possible_outputs = collection_skins[collection_skins["rarity"] == output_rarity]
    # Filters the previous table by the target rarity

    return possible_outputs

def get_output_probabilities(recipe, input_table, possible_outputs):
    collection_quantities = {}
    for skin in recipe:
        quantity = recipe[skin]
        skin_row = input_table[input_table["skin_name"] == skin]
        collection = skin_row["collection"].iloc[0]

        if collection not in collection_quantities:
            collection_quantities[collection] = 0
        
        collection_quantities[collection] += quantity

    output_counts = possible_outputs["collection"].value_counts()

    output_with_probabilities = possible_outputs.copy()

    probabilities = []

    for index, row in output_with_probabilities.iterrows():
        collection = row["collection"]
        number_of_outputs = output_counts[collection]
        collection_weight = collection_quantities[collection] / 10
        
        probability = collection_weight / number_of_outputs

        probabilities.append(probability)

    output_with_probabilities["probability"] = probabilities

    return output_with_probabilities


"""
Profitability Section
"""

def calculate_input_cost(recipe, input_table):
    cost = 0.0
    for index, row in input_table.iterrows():
        skin_name = row["skin_name"]
        price = row["price"]
        quantity = recipe[skin_name]
        
        cost += price * quantity
    
    return cost

def calculate_expected_output(output_probabilities):
    expected_contribution = output_probabilities["price"] * output_probabilities["probability"]

    expected_output = expected_contribution.sum()

    return expected_output

def calculate_expected_profit(expected_output, input_cost):
    return expected_output - input_cost

def calculate_roi(expected_output, input_cost):
    return expected_output / input_cost




input_table = get_input_table(example_recipe, combined_table)
print("Input Table:")
print(input_table)

possible_outputs = get_possible_outputs(input_table, combined_table)

print(f"Output Probabilities:")
print(get_output_probabilities(example_recipe, input_table, possible_outputs))