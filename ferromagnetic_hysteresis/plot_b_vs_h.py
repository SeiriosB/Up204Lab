#!/usr/bin/env python3
"""Generate B vs H graphs for run1 ferromagnetic hysteresis datasets."""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


DATA_DIR = Path(__file__).resolve().parent / "data"
GRAPHS_DIR = Path(__file__).resolve().parent / "graphs"

# H = NI/L formulas from the analysis section
# Non-laminated (soft iron): H = 2586 * I
# Laminated: H = 2459 * I
DATASETS = {
    "run1laminatediron": {
        "title": "Laminated Iron",
        "h_factor": 2459,  # H = 2459 * I
    },
    "run1softiron": {
        "title": "Soft Iron", 
        "h_factor": 2586,  # H = 2586 * I (non-laminated)
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


def plot_b_vs_h(name: str, config: dict, currents: list[float], fluxes: list[float]) -> None:
    """Plot B vs H using the conversion H = h_factor * I."""
    # Convert current to magnetic field strength
    h_values = [config["h_factor"] * i for i in currents]
    
    plt.figure(figsize=(7, 5), dpi=150)
    plt.plot(h_values, fluxes, linewidth=1.0)
    plt.scatter(h_values, fluxes, s=10)
    plt.title(config["title"])
    plt.xlabel("H (A/m)")
    plt.ylabel("B (mT)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = GRAPHS_DIR / f"{name}_b_vs_h.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Generated {output_path.name}")


def main() -> None:
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, config in DATASETS.items():
        path = DATA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset: {path}")
        currents, fluxes = read_dataset(path)
        if not currents:
            raise ValueError(f"No numeric data found in {path}")
        plot_b_vs_h(filename, config, currents, fluxes)


if __name__ == "__main__":
    main()
