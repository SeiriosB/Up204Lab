#!/usr/bin/env python3
"""Find coercive field strength (H at B=0) for ferromagnetic materials."""
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


def find_main_coercivity_crossings(h_values: list[float], b_values: list[float]) -> tuple[float, float]:
    """
    Find the two main B=0 crossings of the hysteresis loop.
    These represent the coercive field strengths.
    """
    h = np.array(h_values)
    b = np.array(b_values)
    
    # Find all B=0 crossings with their positions and H values
    crossings = []
    for i in range(len(b) - 1):
        if (b[i] * b[i+1] <= 0) and (b[i] != b[i+1]):
            h_at_zero = h[i] + (h[i+1] - h[i]) * (-b[i]) / (b[i+1] - b[i])
            # Look at max |H| in a window before this crossing
            window_start = max(0, i - 50)
            max_h_before = np.max(np.abs(h[window_start:i+1]))
            crossings.append((i, h_at_zero, max_h_before))
    
    if not crossings:
        return 0.0, 0.0
    
    # Find crossings with high |H| values (these are on the main loop)
    crossings_sorted = sorted(crossings, key=lambda x: x[2], reverse=True)
    
    # Get the top crossings - they should represent the main hysteresis loop
    main_crossings = []
    for crossing in crossings_sorted:
        h_val = crossing[1]
        # Check if this is a new branch (positive or negative)
        if not main_crossings:
            main_crossings.append(h_val)
        else:
            # Add if it's opposite sign from existing
            if len(main_crossings) == 1:
                if h_val * main_crossings[0] < 0:  # Opposite signs
                    main_crossings.append(h_val)
                    break
    
    if len(main_crossings) >= 2:
        # Identify which is positive and which is negative
        if main_crossings[0] > 0:
            h_plus = main_crossings[0]
            h_minus = main_crossings[1]
        else:
            h_plus = main_crossings[1]
            h_minus = main_crossings[0]
        return h_plus, h_minus
    
    return 0.0, 0.0


def main() -> None:
    print("Finding coercive field strength (H at B=0):\n")
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
        
        h_plus, h_minus = find_main_coercivity_crossings(h_values, fluxes)
        
        print(f"{config['title']}:")
        print(f"  H_+ (descending branch, B→0): {h_plus:.2f} A/m")
        print(f"  H_- (ascending branch, B→0): {h_minus:.2f} A/m")
        print(f"  |H_-| = {abs(h_minus):.2f} A/m")
        
        hc = (h_plus + abs(h_minus)) / 2
        uncertainty = abs(h_plus - abs(h_minus)) / 2
        
        print(f"  H_c = (H_+ + |H_-|)/2 = ({h_plus:.2f} + {abs(h_minus):.2f})/2")
        print(f"      = {hc:.2f} ± {uncertainty:.2f} A/m")
        print()


if __name__ == "__main__":
    main()
