#!/usr/bin/env python3
"""Recalculate hysteresis loop areas with proper analysis."""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


DATA_DIR = Path(__file__).resolve().parent / "data"
GRAPHS_DIR = Path(__file__).resolve().parent / "graphs"

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


def calculate_area_shoelace(h: np.ndarray, b: np.ndarray) -> float:
    """Calculate area using Shoelace formula."""
    n = len(h)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += h[i] * b[j]
        area -= h[j] * b[i]
    return abs(area) / 2.0


def plot_and_analyze(name: str, config: dict, h_values: list[float], b_values: list[float]) -> float:
    """Plot the loop and calculate area."""
    h = np.array(h_values)
    b = np.array(b_values)
    
    # Calculate area
    area = calculate_area_shoelace(h, b)
    
    # Create diagnostic plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=150)
    
    # Plot 1: Full B-H curve
    ax1.plot(h, b, 'b-', linewidth=0.5, alpha=0.7)
    ax1.scatter(h[::50], b[::50], s=20, c='red', alpha=0.5, label='Every 50th point')
    ax1.set_xlabel('H (A/m)')
    ax1.set_ylabel('B (mT)')
    ax1.set_title(f'{config["title"]} - Full Data')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Zoomed view
    # Find approximate extent of main loop
    h_max = np.percentile(np.abs(h), 95)
    b_max = np.percentile(np.abs(b), 95)
    mask = (np.abs(h) <= h_max * 1.1) & (np.abs(b) <= b_max * 1.1)
    
    ax2.plot(h[mask], b[mask], 'b-', linewidth=0.8)
    ax2.set_xlabel('H (A/m)')
    ax2.set_ylabel('B (mT)')
    ax2.set_title(f'{config["title"]} - Main Loop\nArea = {area:.2f} mT·A/m')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = GRAPHS_DIR / f"{name}_area_analysis.png"
    plt.savefig(output_path)
    plt.close()
    
    return area


def main() -> None:
    print("Recalculating hysteresis loop areas:\n")
    print("=" * 80)
    
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
        
        print(f"\n{config['title']}:")
        print(f"  Total data points: {len(h_values)}")
        print(f"  H range: [{min(h_values):.2f}, {max(h_values):.2f}] A/m")
        print(f"  B range: [{min(fluxes):.2f}, {max(fluxes):.2f}] mT")
        
        # Calculate and plot
        area = plot_and_analyze(filename, config, h_values, fluxes)
        area_j_per_m3 = area * 1e-3
        
        results[config["title"]] = {
            "area": area,
            "energy": area_j_per_m3
        }
        
        print(f"  Area: {area:.2f} mT·A/m")
        print(f"  Energy loss per cycle: {area_j_per_m3:.3f} J/m³")
    
    print("\n" + "=" * 80)
    print("\nComparison:")
    print("-" * 80)
    
    if "Laminated Iron" in results and "Soft Iron" in results:
        lam_area = results["Laminated Iron"]["area"]
        soft_area = results["Soft Iron"]["area"]
        ratio = lam_area / soft_area
        
        print(f"Laminated Iron: {lam_area:.2f} mT·A/m = {results['Laminated Iron']['energy']:.3f} J/m³")
        print(f"Soft Iron:      {soft_area:.2f} mT·A/m = {results['Soft Iron']['energy']:.3f} J/m³")
        print(f"\nRatio (Laminated/Soft): {ratio:.3f}")
        
        if ratio > 1:
            print("\n⚠️  WARNING: Laminated iron shows HIGHER area than soft iron!")
            print("   This is physically unexpected. Laminated iron should have lower")
            print("   hysteresis losses. Possible issues:")
            print("   - Data collection artifacts")
            print("   - Incomplete hysteresis loops")
            print("   - Different saturation levels")


if __name__ == "__main__":
    main()
