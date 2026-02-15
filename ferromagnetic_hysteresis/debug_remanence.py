#!/usr/bin/env python3
"""Detailed analysis of H=0 crossings to find remanence."""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


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


def analyze_zero_crossings(h_values: list[float], b_values: list[float], material: str) -> None:
    """Find and display all H=0 crossings in detail."""
    h = np.array(h_values)
    b = np.array(b_values)
    
    print(f"\n{material}:")
    print("=" * 80)
    print(f"Total data points: {len(h)}")
    print(f"H range: [{h.min():.2f}, {h.max():.2f}] A/m")
    print(f"B range: [{b.min():.2f}, {b.max():.2f}] mT")
    
    # Find points very close to H=0
    threshold = 50  # A/m
    near_zero = np.where(np.abs(h) < threshold)[0]
    
    print(f"\nPoints within ±{threshold} A/m of H=0:")
    print(f"{'Index':<8} {'H (A/m)':<15} {'B (mT)':<15}")
    print("-" * 80)
    for idx in near_zero[:20]:  # Show first 20
        print(f"{idx:<8} {h[idx]:<15.2f} {b[idx]:<15.2f}")
    
    # Find actual zero crossings
    print(f"\nZero crossings (sign changes in H):")
    print(f"{'Index':<8} {'H1 (A/m)':<15} {'H2 (A/m)':<15} {'B1 (mT)':<15} {'B2 (mT)':<15} {'B at H=0':<15}")
    print("-" * 100)
    
    zero_crossings = []
    for i in range(len(h) - 1):
        if (h[i] * h[i+1] <= 0) and (h[i] != h[i+1]):  # Sign change
            # Linear interpolation
            b_at_zero = b[i] + (b[i+1] - b[i]) * (-h[i]) / (h[i+1] - h[i])
            zero_crossings.append((i, h[i], h[i+1], b[i], b[i+1], b_at_zero))
            print(f"{i:<8} {h[i]:<15.2f} {h[i+1]:<15.2f} {b[i]:<15.2f} {b[i+1]:<15.2f} {b_at_zero:<15.2f}")
    
    if zero_crossings:
        print(f"\nRemanence values found at H=0:")
        for idx, (i, h1, h2, b1, b2, b_zero) in enumerate(zero_crossings):
            print(f"  Crossing {idx+1}: B = {b_zero:.2f} mT")
        
        if len(zero_crossings) >= 2:
            b_vals = [zc[5] for zc in zero_crossings]
            b_plus = b_vals[0]
            b_minus = b_vals[1]
            
            print(f"\nUsing first two crossings:")
            print(f"  B_+ = {b_plus:.2f} mT")
            print(f"  B_- = {b_minus:.2f} mT")
            print(f"  B_r = (B_+ + |B_-|)/2 = ({b_plus:.2f} + {abs(b_minus):.2f})/2 = {(b_plus + abs(b_minus))/2:.2f} mT")
            print(f"  Uncertainty = |B_+ - |B_-||/2 = {abs(b_plus - abs(b_minus))/2:.2f} mT")
    else:
        print("\nNo clear zero crossings found!")


def main() -> None:
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
        
        analyze_zero_crossings(h_values, fluxes, config["title"])


if __name__ == "__main__":
    main()
