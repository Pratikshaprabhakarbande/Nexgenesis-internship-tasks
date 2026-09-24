# FastBox Logistics Simulator

A robust, production-ready Python simulation engine for **FastBox Logistics**. The simulator models daily package pickup and delivery operations across multiple warehouses and delivery agents, computing total distance traveled, operational efficiency, and identifying the top-performing agent.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Standard Python libraries (no external dependencies required to run the core simulator).
- `pytest` (optional, for running the test suite).

### Execution Command
Run the simulation against any input JSON file (defaults to `base_case.json`):

```bash
python main.py base_case.json
```

### CLI Arguments & Features
```bash
# Run simulation and output report to report.json
python main.py base_case.json

# Specify custom output path
python main.py test_case_1.json --output custom_report.json

# Export top performer metrics to CSV and show ASCII map visualization
python main.py base_case.json --export-csv --ascii
```

---

## 🧪 Testing

Run the full automated test suite covering unit tests and all 10 test case files (`base_case.json`, `test_case_1.json` through `test_case_10.json`):

```bash
python -m pytest
```

Or run standard unittest without third-party dependencies:

```bash
python -m unittest discover -s tests
```

---

## 📐 Explicit Engineering Assumptions

In accordance with assignment instructions, all ambiguous or undefined specification logic has been handled deterministically using the following explicit engineering decisions:

### 1. Input JSON Schema Normalization
- **Flexible Data Parsing**: The simulator automatically handles both structural formats observed across test datasets:
  - **Dictionary format**: `"warehouses": {"W1": [0, 0]}` and `"agents": {"A1": [5, 5]}`
  - **List format**: `"warehouses": [{"id": "W1", "location": [0, 0]}]` and `"agents": [{"id": "A1", "location": [5, 5]}]`
- **Key Aliases**: Supports both `"warehouse"` and `"warehouse_id"` keys inside package objects.

### 2. Package Assignment & Tie-Breaking
- **Nearest Agent Logic**: Each package is assigned to the nearest agent based on Euclidean distance $d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$ from the agent's initial starting location to the package's originating warehouse.
- **Equidistant Tie-Breaking**: If multiple agents are at the exact same distance to a warehouse, the agent with the lexicographically smaller ID (e.g. `"A1"` before `"A2"`) is selected.

### 3. Delivery Routing & Traversal Logic
- **Initial Location**: Each agent begins their day at their starting coordinates provided in the JSON input.
- **Sequential Leg Traversal**: For each assigned package (processed in input/ID order):
  1. Agent travels from their current position to the package's warehouse to pick up the package.
  2. Agent travels from the warehouse to the package's destination to complete delivery.
  3. The agent's current position is updated to the package destination for the next leg.
- **Unassigned Agents**: Agents assigned zero packages record `packages_delivered: 0`, `total_distance: 0.0`, and `efficiency: 0.0`.

### 4. Metrics & Best Agent Selection
- **Efficiency Metric**: Defined as average distance per package delivered:
  $$\text{efficiency} = \frac{\text{total\_distance}}{\text{packages\_delivered}}$$
- **Best Agent Criteria**: The agent with `packages_delivered > 0` achieving the lowest (minimum) efficiency value is selected as `best_agent`.
- **Best Agent Tie-Breaking**: If top agents tie on efficiency, the lexicographically smaller agent ID is selected.
- **Zero Packages Edge Case**: If no packages are delivered across all agents, `best_agent` reports `"N/A"`.

---

## 🎁 Bonus Features

1. **Top Performer CSV Export**: `--export-csv` flag automatically exports the winning agent's metrics to `top_performer.csv`.
2. **ASCII Map Route Visualization**: `--ascii` flag renders a 20x20 visual spatial grid displaying warehouses (`W`), agents (`A`), and package destinations (`P`).

---

## 📁 Repository Structure

```
nexgenesis/
├── src/
│   ├── models.py       # Domain models (Point, Warehouse, Agent, Package)
│   ├── parser.py       # Robust multi-schema JSON parser
│   ├── simulator.py    # Core simulation engine & metrics calculator
│   └── report.py       # Report export, CSV generator, & ASCII visualizer
├── tests/
│   ├── test_parser.py      # Unit tests for JSON parser
│   ├── test_simulator.py   # Unit tests for simulator engine
│   └── test_integration.py # Integration tests for all 10 JSON test cases
├── base_case.json
├── test_case_1.json .. test_case_10.json
├── main.py             # CLI entry point
├── README.md           # Documentation & engineering assumptions
└── requirements.txt    # Project dependencies
```
