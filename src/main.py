import pandas as pd

from load_data import load_prices, load_skins_metadata
from recipe_generator import get_same_rarity_inputs

import tradeup_evaluator as te

prices = load_prices()

skins_metadata = load_skins_metadata()

adjusted_table = te.get_adjusted_table(skins_metadata)

results = []

industrial_grade_pairs = get_same_rarity_inputs(skins_metadata, "Industrial Grade")

for recipe in industrial_grade_pairs:
    te.check_input_skins_exist(recipe, adjusted_table)

    input_table = te.get_input_table(recipe, adjusted_table)
    possible_outputs = te.get_possible_outputs(input_table, adjusted_table)
    unique_breakpoints = te.get_unique_adjusted_breakpoints(possible_outputs)

    for k in range(1, 10):
        output_probabilities = te.get_output_probabilities(recipe, k, input_table, possible_outputs)

        for breakpoint in unique_breakpoints:
            result = te.evaluate_candidate(
                recipe,
                k,
                breakpoint,
                input_table,
                output_probabilities,
                prices
            )

            results.append(result)

results_table = pd.DataFrame(results)

results_table = results_table.sort_values("roi", ascending=False)

results_table.to_csv("data/outputs/opportunities.csv", index=False)