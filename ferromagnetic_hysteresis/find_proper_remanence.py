#!/usr/bin/env python3
"""Find proper remanence by identifying main hysteresis loop crossings."""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np


DATA_DIR = Path(__file__).resolve().parent / "data"

DATASETS = {
    "run1laminatediron": {
        "title": "Laminated Iron",
        "h_factor": 2459,
    },
    "run1softiron": {
        "title": "Soft Iron", 
        "h_factor": 2586,
    },
}


def read_dataset(path: Path) -> tuple[list[float], list[float]]:
    """Read current and flux density data from file."""
    currents: list[float] = []
    fluxes: list[float] = []

    with path.open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            if not row or len(row) < 2:
                continue
            if row[0].strip().lower() in {"current", "i/a"}:
                continue
            if row[1].strip().lower() in {"flux density b", "b/mt"}:
                continue
            try:
                current = float(row[0].strip())
                flux = float(row[1].strip())
            except ValueError:
                continue
            currents.append(current)
            fluxes.append(flux)

    return currents, fluxes


def find_main_hysteresis_crossings(h_values: list[float], b_values: list[float]) -> tuple[float, float]:
    """
    Find the two main H=0 crossings of the hysteresis loop by identifying
    crossings that occur after reaching high/low B values.
    """
    h = np.array(h_values)
    b = np.array(b_values)
    
    # Find all zero crossings with their positions and B values
    crossings = []
    for i in range(len(h) - 1):
        if (h[i] * h[i+1] <= 0) and (h[i] != h[i+1]):
            b_at_zero = b[i] + (b[i+1] - b[i]) * (-h[i]) / (h[i+1] - h[i])
            # Look at max |B| in a window before this crossing
            window_start = max(0, i - 50)
            max_b_before = np.max(np.abs(b[window_start:i+1]))
            crossings.append((i, b_at_zero, max_b_before))
    
    if not crossings:
        return 0.0, 0.0
    
    # Find crossings with high |B| values (these are on the main loop)
    # Sort by the maximum |B| value before the crossing
    crossings_sorted = sorted(crossings, key=lambda x: x[2], reverse=True)
    
    # Get the top crossings - they should represent the main hysteresis loop
    main_crossings = []
    for crossing in crossings_sorted:
        b_val = crossing[1]
        # Check if this is a new branch (positive or negative)
        if not main_crossings:
            main_crossings.append(b_val)
        else:
            # Add if it's opposite sign from existing
            if len(main_crossings) == 1:
                if b_val * main_crossings[0] < 0:  # Opposite signs
                    main_crossings.append(b_val)
                    break
    
    if len(main_crossings) >= 2:
        # Identify which is positive and which is negative
        if main_crossings[0] > 0:
            b_plus = main_crossings[0]
            b_minus = main_crossings[1]
        else:
            b_plus = main_crossings[1]
            b_minus = main_crossings[0]
        return b_plus, b_minus
    
    return 0.0, 0.0


def main() -> None:
    print("Finding main hysteresis loop remanence:\n")
    print("=" * 80)
    
    for filename, config in DATASETS.items():
        path = DATA_DIR / filename
        if not path.exists():
            print(f"Missing dataset: {path}")
            continue
            
        currents, fluxes = read_dataset(path)
        if not currents:
            print(f"No data found in {path}")
            continue
        
        # Convert current to magnetic field strength
        h_values = [config["h_factor"] * i for i in currents]
        
        b_plus, b_minus = find_main_hysteresis_crossings(h_values, fluxes)
        
        print(f"{config['title']}:")
        print(f"  B_+ (descending branch, H→0): {b_plus:.2f} mT")
        print(f"  B_- (ascending branch, H→0): {b_minus:.2f} mT")
        print(f"  |B_-| = {abs(b_minus):.2f} mT")
        
        br = (b_plus + abs(b_minus)) / 2
        uncertainty = abs(b_plus - abs(b_minus)) / 2
        
        print(f"  B_r = (B_+ + |B_-|)/2 = ({b_plus:.2f} + {abs(b_minus):.2f})/2")
        print(f"      = {br:.2f} ± {uncertainty:.2f} mT")
        print()


if __name__ == "__main__":
    main()
