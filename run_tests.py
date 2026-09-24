"""Run all supplied Nexgensis JSON cases against main.solve().

The supplied files include base_case.json and test_case_1, 3-10.
No test_case_2.json was available in the provided test files, so it is not invented.
"""
import json
from pathlib import Path
from main import solve

ROOT = Path(__file__).parent
CASES = [ROOT / "base_case.json"] + [ROOT / f"test_case_{i}.json" for i in range(1, 11)]
CASES = [path for path in CASES if path.exists()]

for path in CASES:
    data = json.loads(path.read_text(encoding="utf-8"))
    result = solve(data)

    expected_agents = (
        set(data["agents"])
        if isinstance(data["agents"], dict)
        else {agent["id"] for agent in data["agents"]}
    )
    assert len(result["assignments"]) == len(data["packages"])
    assert set(result["final_agent_locations"]) == expected_agents
    assert result["total_distance"] >= 0

    for assignment in result["assignments"]:
        assert assignment["package_id"]
        assert assignment["agent_id"]
        assert assignment["warehouse_id"]
        assert len(assignment["route"]) == 3

    print(f"PASS {path.name}: {len(result['assignments'])} packages, total={result['total_distance']}")

print(f"\nPassed {len(CASES)} available input cases.")
