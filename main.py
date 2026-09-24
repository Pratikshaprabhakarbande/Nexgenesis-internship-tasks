"""Greedy multi-agent package delivery planner.

The planner assigns each package, in input order, to the available agent
with the smallest immediate travel cost:
    current agent position -> package warehouse -> destination.

After delivery, the selected agent is considered to be at the destination.
This is a deterministic, online dispatch policy suitable for the supplied
problem model when no global routing/capacity rule is specified.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def distance(a: list[float], b: list[float]) -> float:
    """Return Euclidean distance between two 2-D points."""
    if len(a) != 2 or len(b) != 2:
        raise ValueError("Coordinates must contain exactly two values.")
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _normalise(
    data: dict[str, Any],
) -> tuple[dict[str, list[float]], dict[str, list[float]], list[dict[str, Any]]]:
    warehouses_raw = data.get("warehouses", {})
    agents_raw = data.get("agents", {})
    packages = data.get("packages", [])

    # The supplied base case uses lists of {id, location}; generated cases
    # use ID -> coordinate mappings. Accept both representations.
    if isinstance(warehouses_raw, list):
        warehouses = {item["id"]: item["location"] for item in warehouses_raw}
    else:
        warehouses = warehouses_raw

    if isinstance(agents_raw, list):
        agents = {item["id"]: item["location"] for item in agents_raw}
    else:
        agents = agents_raw

    if not isinstance(warehouses, dict) or not isinstance(agents, dict) or not isinstance(packages, list):
        raise ValueError("Input must contain warehouses, agents and packages.")

    normalised_packages = []
    for package in packages:
        warehouse_id = package.get("warehouse_id", package.get("warehouse"))
        if not package.get("id") or warehouse_id is None or "destination" not in package:
            raise ValueError(f"Invalid package: {package!r}")
        normalised_packages.append(
            {
                "id": package["id"],
                "warehouse_id": warehouse_id,
                "destination": package["destination"],
            }
        )

    return warehouses, agents, normalised_packages


def solve(data: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic delivery plan for the supplied scenario."""
    warehouses, agents, packages = _normalise(data)

    if not agents and packages:
        raise ValueError("At least one agent is required when packages exist.")

    positions = {agent_id: list(location) for agent_id, location in agents.items()}
    assignments = []
    total_distance = 0.0

    for package in packages:
        warehouse_id = package["warehouse_id"]
        if warehouse_id not in warehouses:
            raise ValueError(
                f"Package {package['id']} references unknown warehouse {warehouse_id!r}."
            )

        warehouse = warehouses[warehouse_id]
        destination = package["destination"]
        candidates = []

        for agent_id in sorted(positions):
            start = positions[agent_id]
            to_warehouse = distance(start, warehouse)
            warehouse_to_destination = distance(warehouse, destination)
            trip_distance = to_warehouse + warehouse_to_destination
            candidates.append((trip_distance, agent_id))

        trip_distance, agent_id = min(candidates)

        start = list(positions[agent_id])
        positions[agent_id] = list(destination)
        total_distance += trip_distance

        assignments.append(
            {
                "package_id": package["id"],
                "agent_id": agent_id,
                "warehouse_id": warehouse_id,
                "distance": round(trip_distance, 6),
                "route": [start, list(warehouse), list(destination)],
            }
        )

    return {
        "assignments": assignments,
        "total_distance": round(total_distance, 6),
        "final_agent_locations": {
            agent_id: position for agent_id, position in sorted(positions.items())
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan package deliveries.")
    parser.add_argument("input", type=Path, help="Path to the scenario JSON file.")
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8") as file:
        data = json.load(file)

    print(json.dumps(solve(data), indent=2))


if __name__ == "__main__":
    main()
