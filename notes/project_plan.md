Yes. We’ll make this **extremely step-by-step**. Do **not** think about APIs, Steam, CSFloat, inventory scanning, or Casemove yet.

Your first goal is only:

> Build a tiny tradeup finder that takes manually entered data and outputs ranked tradeups.

Copy this into a file called:

```text
notes/project_plan.md
```

# CS2 Tradeup Finder To-Do List

## Phase 0 — Understand the first goal

### 0.1 Define the first version

Goal:

```text
Given a small list of skins, prices, floats, and possible outputs,
generate simple 2-skin tradeup recipes and rank them by EV.
```

Done when you can explain the project as:

```text
I input skin data manually.
The program tests 2-skin tradeups.
It outputs a table of profitable-looking opportunities.
```

---

### 0.2 Decide what to ignore for now

Ignore:

```text
Steam API
CSFloat API
inventory scanning
storage units
Steam buy orders
float checking APIs
backtesting
automatic tradeup execution
```

Done when you accept that Version 1 is **manual data in, ranked table out**.

---

## Phase 1 — Create the project folder

### 1.1 Create a folder

Create a folder called:

```text
cs2-tradeup-finder
```

Done when the folder exists on your computer.

---

### 1.2 Open the folder in VS Code

Open `cs2-tradeup-finder` in VS Code.

Done when VS Code is showing that folder.

---

### 1.3 Create a GitHub repo

Create a GitHub repository called:

```text
cs2-tradeup-finder
```

Done when the repo exists on GitHub.

---

### 1.4 Connect your local folder to GitHub

Connect the local folder to the GitHub repo.

Done when you can push changes to GitHub.

---

## Phase 2 — Create the basic files

### 2.1 Create `README.md`

Create:

```text
README.md
```

Done when the file exists.

---

### 2.2 Write one paragraph in `README.md`

Write:

```text
This project searches for profitable CS2 tradeup contracts.
The first version uses manual skin and price data, generates simple two-skin recipes, evaluates EV and risk, and outputs ranked opportunities.
```

Done when the README says what the project does.

---

### 2.3 Create `.gitignore`

Create:

```text
.gitignore
```

Done when the file exists.

---

### 2.4 Add basic ignored files

Add things like:

```text
__pycache__/
.env
.ipynb_checkpoints/
```

Done when Python junk files will not be pushed to GitHub.

---

### 2.5 Create `requirements.txt`

Create:

```text
requirements.txt
```

Done when the file exists.

---

### 2.6 Add first packages

Add:

```text
pandas
numpy
```

Done when your package list exists.

---

## Phase 3 — Create the folder structure

### 3.1 Create `data/`

Create:

```text
data/
```

Done when the folder exists.

---

### 3.2 Create data subfolders

Inside `data/`, create:

```text
raw/
processed/
outputs/
```

Done when you have:

```text
data/raw/
data/processed/
data/outputs/
```

---

### 3.3 Create `src/`

Create:

```text
src/
```

Done when the folder exists.

---

### 3.4 Create `notes/`

Create:

```text
notes/
```

Done when the folder exists.

---

### 3.5 Create `tests/`

Create:

```text
tests/
```

Done when the folder exists.

---

### 3.6 Create `notebooks/`

Create:

```text
notebooks/
```

Done when the folder exists.

---

## Phase 4 — Create the planning notes

### 4.1 Create `notes/project_plan.md`

Create:

```text
notes/project_plan.md
```

Done when this to-do list is pasted there.

---

### 4.2 Create `notes/assumptions.md`

Create:

```text
notes/assumptions.md
```

Done when the file exists.

---

### 4.3 Add first assumptions

Write:

```text
Version 1 assumptions:
- Manual price data only.
- No Steam API.
- No CSFloat API.
- Only normal non-StatTrak tradeups.
- Only 10-item tradeups.
- Only two-skin recipes.
- No Steam fees yet.
- No liquidity filter yet.
```

Done when you know what Version 1 is and is not doing.

---

### 4.4 Create `notes/tradeup_ideas.md`

Create:

```text
notes/tradeup_ideas.md
```

Done when you have somewhere to write manual observations from TradeUpSpy/calculators.

---

## Phase 5 — Create tiny manual data files

### 5.1 Create `data/raw/skins_metadata.csv`

Create:

```text
data/raw/skins_metadata.csv
```

Done when the file exists.

---

### 5.2 Decide the columns for skin metadata

The columns should be:

```text
skin_name
collection
rarity
min_float
max_float
stattrak
```

Done when the CSV has these headers.

---

### 5.3 Add 2 input skins manually

Pick two Industrial Grade skins manually.

Add their:

```text
skin_name
collection
rarity
min_float
max_float
stattrak
```

Done when the file has 2 input skins.

---

### 5.4 Add their possible output skins manually

For each input skin’s collection, add the possible Mil-Spec outputs.

Done when your metadata file contains both the inputs and their outputs.

---

### 5.5 Create `data/raw/prices.csv`

Create:

```text
data/raw/prices.csv
```

Done when the file exists.

---

### 5.6 Decide the columns for prices

The columns should be:

```text
skin_name
wear
price
volume
```

Done when the CSV has these headers.

---

### 5.7 Add manual prices

Add prices for:

```text
the 2 input skins
all possible output skins
```

Done when every skin in your tiny test has a price.

---

## Phase 6 — Create the source files

### 6.1 Create `src/main.py`

Create:

```text
src/main.py
```

Purpose:

```text
Run the whole program.
```

Done when the file exists.

---

### 6.2 Create `src/config.py`

Create:

```text
src/config.py
```

Purpose:

```text
Store project settings and assumptions.
```

Done when the file exists.

---

### 6.3 Create `src/load_data.py`

Create:

```text
src/load_data.py
```

Purpose:

```text
Load CSV files.
```

Done when the file exists.

---

### 6.4 Create `src/recipe_generator.py`

Create:

```text
src/recipe_generator.py
```

Purpose:

```text
Generate possible 2-skin recipes.
```

Done when the file exists.

---

### 6.5 Create `src/tradeup_evaluator.py`

Create:

```text
src/tradeup_evaluator.py
```

Purpose:

```text
Evaluate one tradeup recipe.
```

Done when the file exists.

---

### 6.6 Create `src/metrics.py`

Create:

```text
src/metrics.py
```

Purpose:

```text
Calculate EV, ROI, variance, chance to profit, and score.
```

Done when the file exists.

---

### 6.7 Create `src/export_results.py`

Create:

```text
src/export_results.py
```

Purpose:

```text
Save final opportunities to CSV.
```

Done when the file exists.

---

## Phase 7 — Build the simplest data loader

### 7.1 Load `skins_metadata.csv`

Make the project read:

```text
data/raw/skins_metadata.csv
```

Done when the program can print the skin metadata table.

---

### 7.2 Load `prices.csv`

Make the project read:

```text
data/raw/prices.csv
```

Done when the program can print the price table.

---

### 7.3 Check the columns

Make sure the program checks that required columns exist.

Done when the program warns you if a column is missing.

---

### 7.4 Merge skin metadata with prices

Combine metadata and prices using:

```text
skin_name
```

Done when each skin row has both metadata and price.

---

## Phase 8 — Build one manual tradeup evaluation

### 8.1 Hardcode one recipe manually

Use something like:

```text
7 × Skin A
3 × Skin B
```

Done when the recipe exists inside the program.

---

### 8.2 Calculate input cost

Formula:

```text
input_cost = 7 × price_A + 3 × price_B
```

Done when the program prints the input cost.

---

### 8.3 Find possible outputs

For Skin A, find all next-rarity outputs from its collection.

For Skin B, find all next-rarity outputs from its collection.

Done when the program lists possible outputs.

---

### 8.4 Calculate output probabilities

If the recipe is:

```text
7 × Skin A
3 × Skin B
```

then Skin A’s collection contributes 70% probability mass.

Skin B’s collection contributes 30% probability mass.

Done when output probabilities sum to 1.

---

### 8.5 Calculate expected output value

Formula:

```text
expected_output_value = sum(probability × output_price)
```

Done when the program prints expected output value.

---

### 8.6 Calculate expected profit

Formula:

```text
expected_profit = expected_output_value - input_cost
```

Done when the program prints expected profit.

---

### 8.7 Calculate ROI

Formula:

```text
ROI = expected_profit / input_cost
```

Done when the program prints ROI.

---

## Phase 9 — Add output risk metrics

### 9.1 Calculate profit for each output

For each possible output:

```text
output_profit = output_price - input_cost
```

Done when every output has a profit/loss number.

---

### 9.2 Calculate chance to profit

Add up probabilities where:

```text
output_profit > 0
```

Done when the program prints chance to profit.

---

### 9.3 Calculate worst-case profit

Find the minimum output profit.

Done when the program prints worst-case loss/profit.

---

### 9.4 Calculate standard deviation

Calculate spread of output values around expected output value.

Done when the program prints standard deviation.

---

### 9.5 Calculate a simple score

Use:

```text
score = expected_profit / standard_deviation
```

Done when the program prints a score.

---

## Phase 10 — Generate all two-skin recipes

### 10.1 Pick eligible input skins

Filter to only:

```text
Industrial Grade
non-StatTrak
```

Done when your program has a list of input candidates.

---

### 10.2 Generate pairs

Generate pairs:

```text
Skin A, Skin B
```

Done when the program prints possible pairs.

---

### 10.3 Generate ratios

For each pair, generate:

```text
1 A + 9 B
2 A + 8 B
3 A + 7 B
...
9 A + 1 B
```

Done when each pair creates 9 recipes.

---

### 10.4 Evaluate each recipe

Run your evaluator on every recipe.

Done when every recipe has EV, ROI, chance to profit, worst case, standard deviation, and score.

---

## Phase 11 — Export results

### 11.1 Create a results table

Each row should include:

```text
recipe
input_cost
expected_output_value
expected_profit
roi
chance_to_profit
worst_case_profit
standard_deviation
score
```

Done when these columns exist.

---

### 11.2 Sort results

Sort by:

```text
score descending
```

or:

```text
expected_profit descending
```

Done when best-looking tradeups appear at the top.

---

### 11.3 Save to CSV

Save the table as:

```text
data/outputs/opportunities.csv
```

Done when the file appears.

---

### 11.4 Open the CSV manually

Open it in Excel, Numbers, or Google Sheets.

Done when you can visually inspect ranked tradeups.

---

## Phase 12 — Validate against a calculator

### 12.1 Pick one recipe from your output

Choose one recipe from:

```text
opportunities.csv
```

Done when you have selected one tradeup.

---

### 12.2 Enter it into TradeUpSpy or another calculator

Manually enter the same recipe.

Done when the calculator gives EV/probabilities.

---

### 12.3 Compare output probabilities

Check:

```text
Do my output probabilities match the calculator?
```

Done when probabilities match or you understand why they differ.

---

### 12.4 Compare expected value

Check:

```text
Does my EV roughly match the calculator?
```

Done when your EV is close.

---

### 12.5 Fix mistakes

If anything differs, fix one issue at a time.

Done when one recipe matches the calculator.

---

## Phase 13 — Add adjusted float

### 13.1 Add actual float to input data

Add a column somewhere for:

```text
actual_float
```

Done when each input skin in a recipe has an actual float.

---

### 13.2 Calculate adjusted float

Formula:

```text
adjusted_float = (actual_float - min_float) / (max_float - min_float)
```

Done when the program prints adjusted float for each input.

---

### 13.3 Calculate average adjusted float

Average the adjusted floats across all 10 inputs.

Done when the program prints average adjusted float.

---

### 13.4 Calculate output float

Formula:

```text
output_float = output_min + average_adjusted_float × (output_max - output_min)
```

Done when every possible output has a predicted float.

---

### 13.5 Add output wear category

Classify output float into:

```text
Factory New
Minimal Wear
Field-Tested
Well-Worn
Battle-Scarred
```

Done when each output has a predicted wear.

---

### 13.6 Use wear-specific prices

Instead of one output price, use the price for the predicted output wear.

Done when EV changes depending on float.

---

## Phase 14 — Improve the results table

### 14.1 Add average adjusted float

Add column:

```text
average_adjusted_float
```

Done when it appears in `opportunities.csv`.

---

### 14.2 Add output wear summary

Add column:

```text
output_wears
```

Done when you can see whether the tradeup produces FN/MW/etc.

---

### 14.3 Add best output

Add column:

```text
best_output
```

Done when the table shows the most profitable output.

---

### 14.4 Add worst output

Add column:

```text
worst_output
```

Done when the table shows the worst output.

---

### 14.5 Add number of outputs

Add column:

```text
num_outputs
```

Done when you know how many outcomes the recipe has.

---

## Phase 15 — Add filters

### 15.1 Add minimum EV filter

Only keep recipes where:

```text
expected_profit > 0
```

Done when negative EV trades disappear.

---

### 15.2 Add minimum ROI filter

Example:

```text
ROI > 0.02
```

Done when tiny-edge trades disappear.

---

### 15.3 Add max input cost filter

Example:

```text
input_cost <= £10
```

Done when expensive trades disappear.

---

### 15.4 Add chance-to-profit filter

Example:

```text
chance_to_profit >= 0.5
```

Done when jackpot-only trades disappear.

---

### 15.5 Add worst-case loss filter

Example:

```text
worst_case_profit >= -£1
```

Done when very risky trades disappear.

---

## Phase 16 — Make the project nicer to use

### 16.1 Put settings in `config.py`

Move things like:

```text
rarity
minimum_roi
maximum_input_cost
minimum_chance_to_profit
```

into `config.py`.

Done when you can change assumptions in one place.

---

### 16.2 Add clear terminal messages

Make the program print things like:

```text
Loaded 20 skins.
Generated 180 recipes.
Found 12 positive EV recipes.
Saved results to data/outputs/opportunities.csv.
```

Done when running the program feels understandable.

---

### 16.3 Add error messages

Examples:

```text
Missing price for output skin X.
Probabilities do not sum to 1.
No eligible input skins found.
```

Done when mistakes are easy to diagnose.

---

## Phase 17 — Add tests later

Do not start here, but eventually:

### 17.1 Test adjusted float

Check a known example manually.

Done when the formula gives the expected number.

---

### 17.2 Test probabilities sum to 1

Every recipe should have:

```text
total_probability = 1
```

Done when this is automatically checked.

---

### 17.3 Test input cost

For:

```text
7 × A + 3 × B
```

check that cost is:

```text
7 price_A + 3 price_B
```

Done when this test passes.

---

### 17.4 Test EV

Use a tiny fake example where you know the answer.

Done when EV calculation is verified.

---

## Phase 18 — Only after Version 1 works

Do these later, not now.

### 18.1 Add more skins

Expand from 2 input skins to 10.

---

### 18.2 Add all Industrial Grade skins

Expand to full Industrial → Mil-Spec search.

---

### 18.3 Add liquidity

Add volume/spread columns.

---

### 18.4 Add Steam fees

Account for buying/selling costs.

---

### 18.5 Add Steam buy-order float wastage

Estimate usable float probability.

---

### 18.6 Add API price fetching

Pull live prices.

---

### 18.7 Add inventory scanner

Classify owned items.

---

### 18.8 Add Casemove integration

Move rejected asset IDs.

---

# The exact order you should follow

For now, only do this:

```text
1. Create project folder.
2. Create GitHub repo.
3. Create README.md.
4. Create folder structure.
5. Create tiny metadata CSV.
6. Create tiny prices CSV.
7. Load the CSVs.
8. Evaluate one hardcoded tradeup.
9. Export one result.
10. Only then generate many recipes.
```

Do **not** jump ahead.

A good next prompt to use is:

```text
I am on Step 1.1 of my CS2 tradeup finder project. Walk me through only this step. Do not go ahead.
```
