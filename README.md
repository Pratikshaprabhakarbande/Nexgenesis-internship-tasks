# Nexgensis Python Assignment

A small, deterministic Python solution for assigning delivery packages to agents.

## Run

```bash
python main.py base_case.json
```

For another scenario:

```bash
python main.py test_case_1.json
```

## Approach

For each package, in the order supplied by the input:

1. Find the package's warehouse.
2. Calculate each agent's immediate travel distance:
   `agent position -> warehouse -> package destination`.
3. Assign the package to the agent with the smallest distance.
4. Move that agent's current position to the delivered package destination.
5. Continue with the next package.

Euclidean distance is used because the input provides 2-D coordinates and no road/network model is specified.

## Assumptions

The assignment email asks candidates to make and document reasonable engineering decisions for undefined routing, tie-breaking, and edge cases.

- Package processing follows input order when no explicit routing order is supplied.
- If two agents have the same travel cost, the lexicographically smaller agent ID is selected. This makes results deterministic.
- An agent's position becomes the package destination after delivery.
- No capacity or collision constraints are assumed because none are represented in the supplied input model.
- Both supported input shapes are accepted: the base case uses lists of objects, while generated cases use ID-to-coordinate mappings.

The implementation intentionally avoids hardcoded IDs, coordinates, or test-specific outputs.
