#!/usr/bin/env python3
"""Calculate remanence (B at H=0) for ferromagnetic materials."""
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


def find_remanence(h_values: list[float], b_values: list[float]) -> tuple[float, float]:
    """
    Find remanence: the value of B when H crosses zero.
    Returns the B values at H=0 crossings (positive and negative branches).
    """
    h = np.array(h_values)
    b = np.array(b_values)
    
    # Find where H crosses zero
    zero_crossings = []
    
    for i in range(len(h) - 1):
        # Check if H crosses zero between consecutive points
        if (h[i] <= 0 <= h[i+1]) or (h[i+1] <= 0 <= h[i]):
            # Linear interpolation to find B at H=0
            if h[i+1] != h[i]:
                b_at_zero = b[i] + (b[i+1] - b[i]) * (0 - h[i]) / (h[i+1] - h[i])
                zero_crossings.append(b_at_zero)
    
    if len(zero_crossings) >= 2:
        # Return both remanence values (positive and negative branches)
        return zero_crossings[0], zero_crossings[1]
    elif len(zero_crossings) == 1:
        return zero_crossings[0], zero_crossings[0]
    else:
        # If no clear crossing, find the point closest to H=0
        closest_idx = np.argmin(np.abs(h))
        return b[closest_idx], b[closest_idx]


def main() -> None:
    print("Calculating remanence values:\n")
    print("=" * 70)
    
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
        
        # Find remanence
        b_plus, b_minus = find_remanence(h_values, fluxes)
        
        # Calculate remanence using B_r = (B_+ + |B_-|) / 2
        br_avg = (b_plus + abs(b_minus)) / 2
        
        # Calculate uncertainty as half the difference
        uncertainty = abs(b_plus - abs(b_minus)) / 2
        
        print(f"{config['title']}:")
        print(f"  B_+ (H=0, positive branch): {b_plus:.2f} mT")
        print(f"  B_- (H=0, negative branch): {b_minus:.2f} mT")
        print(f"  |B_-| = {abs(b_minus):.2f} mT")
        print(f"  B_r = (B_+ + |B_-|) / 2 = {br_avg:.2f} ± {uncertainty:.2f} mT")
        print()
    
    print("=" * 70)


if __name__ == "__main__":
    main()
