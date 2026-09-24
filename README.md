# Nexgensis Python Assignment

A small, deterministic Python solution for assigning delivery packages to available agents.

## Run

```bash
python main.py base_case.json
python main.py test_case_1.json
```

Run the supplied test cases with:

```bash
python run_tests.py
```

## Approach

For each package, in the order supplied by the input:

1. Find the package's warehouse.
2. Calculate each agent's immediate travel distance:
   `agent position -> warehouse -> package destination`.
3. Assign the package to the agent with the smallest total distance.
4. Move the selected agent's current position to the package destination.
5. Continue with the next package.

Euclidean distance is used because the input provides 2-D coordinates and does not define a road/network model.

## Explicit Engineering Assumptions

The assignment asks candidates to make and document reasonable decisions for undefined routing order, tie-breaking, and edge cases. The implementation uses these assumptions:

- **Routing / package order:** Packages are processed in the exact order provided in the `packages` array. This keeps the planner deterministic when no global routing order is specified.
- **Agent selection:** For every package, choose the agent with the smallest immediate distance from the agent's current position to the warehouse and then to the destination.
- **Tie-breaking:** If multiple agents have exactly the same travel distance, select the lexicographically smaller agent ID. This guarantees deterministic output.
- **Agent movement:** After delivery, the selected agent's current position becomes that package's destination. The next package therefore uses the updated position.
- **Capacity:** No agent capacity limit is assumed because no capacity field or constraint is represented in the supplied input model.
- **Collisions:** No collision/traffic constraints are assumed because the input provides coordinates but no time, road, or collision model.
- **Distance model:** Straight-line Euclidean distance is used; no road-network or obstacle constraints are assumed.
- **Invalid references:** A package referring to an unknown warehouse raises a clear `ValueError` rather than silently producing an incorrect result.
- **Input shapes:** The solution accepts both the base-case list-of-objects format and the generated ID-to-coordinate mapping format.
- **Missing test case:** The supplied test set contains `base_case.json` and `test_case_1.json`, `test_case_3.json` through `test_case_10.json`. No `test_case_2.json` was invented or assumed.

These assumptions are intentionally documented here so the behavior is transparent and reproducible.

## Output

The program prints JSON containing:

- `assignments` — package, selected agent, warehouse, distance, and route
- `total_distance` — total delivery travel distance
- `final_agent_locations` — final position of every agent

## Testing

`run_tests.py` executes every supplied JSON case available in the repository and checks:

- every package receives exactly one assignment;
- all agents remain represented in the final-location output;
- assignment fields and three-point routes are present;
- calculated total distance is non-negative.

See `TEST_RESULTS.md` for the recorded results.
