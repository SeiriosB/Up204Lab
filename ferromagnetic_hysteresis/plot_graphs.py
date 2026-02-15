#!/usr/bin/env python3
"""Generate B vs I graphs for ferromagnetic hysteresis datasets."""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


DATA_DIR = Path(__file__).resolve().parent / "data"
GRAPHS_DIR = Path(__file__).resolve().parent / "graphs"

DATASETS = {
    "run1laminatediron": "Laminated Iron",
    "run1softiron": "Soft Iron",
    "run2laminatediron": "Laminated Iron",
    "run2softiron": "Soft Iron",
}


def read_dataset(path: Path) -> tuple[list[float], list[float]]:
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


def plot_dataset(name: str, title: str, currents: list[float], fluxes: list[float]) -> None:
    plt.figure(figsize=(7, 5), dpi=150)
    plt.plot(currents, fluxes, linewidth=1.0)
    plt.scatter(currents, fluxes, s=10)
    plt.title(title)
    plt.xlabel("I (A)")
    plt.ylabel("B (mT)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = GRAPHS_DIR / f"{name}_b_vs_i.png"
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, title in DATASETS.items():
        path = DATA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset: {path}")
        currents, fluxes = read_dataset(path)
        if not currents:
            raise ValueError(f"No numeric data found in {path}")
        plot_dataset(filename, title, currents, fluxes)


if __name__ == "__main__":
    main()
