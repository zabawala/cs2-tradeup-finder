import pandas as pd

from load_data import load_prices, load_skins_metadata
from recipe_generator import get_same_rarity_inputs

import tradeup_evaluator as te


def main():
    prices = load_prices()
    prices = te.create_price_lookup(prices)

    skins_metadata = load_skins_metadata()

    adjusted_table = te.get_adjusted_table(skins_metadata)

    roi_results = []
    score_results = []

    industrial_grade_pairs = get_same_rarity_inputs(skins_metadata, "Industrial Grade")

    for recipe in industrial_grade_pairs:
        te.check_input_skins_exist(recipe, adjusted_table)

        input_table = te.get_input_table(recipe, adjusted_table)
        possible_outputs = te.get_possible_outputs(input_table, adjusted_table)
        unique_breakpoints = te.get_unique_adjusted_breakpoints(possible_outputs)
        
        best_roi_candidate = None
        best_score_candidate = None

        for breakpoint in unique_breakpoints:
            input_with_float_and_wear = te.get_input_float_and_wear(breakpoint, input_table)
            input_with_prices = te.get_input_prices(input_with_float_and_wear, prices)

            if te.has_missing_prices(input_with_prices):
                continue

            output_with_float_and_wear = te.get_output_float_and_wear(breakpoint, possible_outputs)
            output_with_prices = te.get_output_prices(output_with_float_and_wear, prices)

            if te.has_missing_prices(output_with_prices):
                continue

            collection_expected_value = te.get_collection_expected_values(output_with_prices)
            for k in range(1, 10):
                expected_output = te.compute_expected_output_from_collections(recipe, k, input_table, collection_expected_value)
            
                result = te.evaluate_candidate(
                    recipe,
                    k,
                    breakpoint,
                    input_with_prices,
                    expected_output
                )

                if best_roi_candidate == None:
                    best_roi_candidate = result
                elif result["roi"] > best_roi_candidate["roi"]:
                    best_roi_candidate = result

                if best_score_candidate == None:
                    best_score_candidate = result
                elif result["score"] > best_score_candidate["score"]:
                    best_score_candidate = result
            
        if best_roi_candidate is not None:
            roi_results.append(best_roi_candidate)

        if best_score_candidate is not None:
            score_results.append(best_score_candidate)


    if not roi_results:
        print("No valid ROI results found. Probably missing too many prices.")
        return

    if not score_results:
        print("No valid score results found. Probably missing too many prices.")
        return

    roi_results_table = pd.DataFrame(roi_results)

    roi_results_table = roi_results_table.sort_values("roi", ascending=False)

    t20_roi = roi_results_table[0:20]

    t20_roi.to_csv("data/outputs/t20_roi.csv", index=False)

    score_results_table = pd.DataFrame(score_results)

    score_results_table = score_results_table.sort_values("score", ascending=False)

    t20_score = score_results_table[0:20]

    t20_score.to_csv("data/outputs/t20_score.csv", index=False)

main()