"""
Main CLI entry point for FastBox Logistics Simulator.

Usage:
    python main.py [input_file.json] [--output report.json] [--export-csv] [--ascii]
"""

import argparse
import json
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parser import load_input_data
from src.simulator import LogisticsSimulator
from src.report import save_report_json, export_top_performer_csv, generate_ascii_map



def run(input_path: str = "base_case.json", output_path: str = "report.json", export_csv: bool = True, ascii_map: bool = False) -> dict:
    """Execute the full simulation pipeline."""
    # Step 1: Parse JSON input
    warehouses, agents, packages = load_input_data(input_path)

    # Step 2: Initialize simulator & run simulation
    simulator = LogisticsSimulator(warehouses, agents, packages)
    report = simulator.run_simulation()

    # Step 3: Save report JSON
    save_report_json(report, output_path)

    # Step 4: Optional bonus exports
    if export_csv:
        export_top_performer_csv(report, "top_performer.csv")

    if ascii_map:
        print(generate_ascii_map(warehouses, agents, packages))

    return report


def main():
    parser = argparse.ArgumentParser(description="FastBox Logistics Simulator")
    parser.add_argument("input_file", nargs="?", default="base_case.json", help="Path to input JSON file")
    parser.add_argument("--output", "-o", default="report.json", help="Path to output JSON report file")
    parser.add_argument("--export-csv", action="store_true", help="Export top performer to CSV")
    parser.add_argument("--ascii", action="store_true", help="Display ASCII visualization of entities")

    args = parser.parse_args()

    try:
        report = run(
            input_path=args.input_file,
            output_path=args.output,
            export_csv=args.export_csv,
            ascii_map=args.ascii
        )
        print(json.dumps(report, indent=4))
    except Exception as e:
        print(f"Error executing simulation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
