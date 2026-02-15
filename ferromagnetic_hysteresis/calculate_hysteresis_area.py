#!/usr/bin/env python3
"""Calculate the area under B vs H hysteresis curves."""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np


DATA_DIR = Path(__file__).resolve().parent / "data"

# H = NI/L formulas from the analysis section
DATASETS = {
    "run1laminatediron": {
        "title": "Laminated Iron",
        "h_factor": 2459,  # H = 2459 * I (A/m)
    },
    "run1softiron": {
        "title": "Soft Iron", 
        "h_factor": 2586,  # H = 2586 * I (A/m, non-laminated)
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


def calculate_hysteresis_area(h_values: list[float], b_values: list[float]) -> float:
    """
    Calculate the area enclosed by the hysteresis loop using the Shoelace formula.
    
    Area represents energy loss per unit volume per cycle.
    B is in mT, H is in A/m
    Area will be in mT·A/m = 10^-3 T·A/m = 10^-3 J/m³
    """
    if len(h_values) < 3 or len(b_values) < 3:
        return 0.0
    
    # Use numpy's trapz for numerical integration
    # For a closed loop, we use the shoelace formula
    h = np.array(h_values)
    b = np.array(b_values)
    
    # Shoelace formula for polygon area
    # Area = 0.5 * |sum(x_i * y_{i+1} - x_{i+1} * y_i)|
    n = len(h)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += h[i] * b[j]
        area -= h[j] * b[i]
    
    return abs(area) / 2.0


def main() -> None:
    print("Calculating hysteresis loop areas:\n")
    print("=" * 70)
    
    results = {}
    
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
        
        # Calculate area
        area = calculate_hysteresis_area(h_values, fluxes)
        
        # Convert to J/m³ (since B is in mT and H is in A/m)
        # Area in mT·A/m = 10^-3 J/m³
        area_j_per_m3 = area * 1e-3
        
        results[config["title"]] = {
            "area_raw": area,
            "area_j_per_m3": area_j_per_m3
        }
        
        print(f"{config['title']}:")
        print(f"  Area under B-H curve: {area:.2f} mT·A/m")
        print(f"  Energy loss per cycle: {area_j_per_m3:.3f} J/m³")
        print()
    
    print("=" * 70)
    print("\nLaTeX formatted results:")
    print("-" * 70)
    
    for material, data in results.items():
        print(f"{material}: {data['area_raw']:.2f} \\text{{ mT·A/m}} = {data['area_j_per_m3']:.3f} \\text{{ J/m}}^3")


if __name__ == "__main__":
    main()
