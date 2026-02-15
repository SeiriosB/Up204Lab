#!/usr/bin/env python3
"""Negate all readings in run2softiron dataset."""
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "run2softiron"

def negate_dataset():
    """Read the dataset, negate all numeric values, and write back."""
    with DATA_FILE.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    
    output_lines = []
    for line in lines:
        # Keep header lines unchanged
        if not line.strip() or "\t" not in line:
            output_lines.append(line)
            continue
        
        parts = line.strip().split("\t")
        if len(parts) != 2:
            output_lines.append(line)
            continue
        
        # Check if this is a header row
        if any(keyword in parts[0].lower() for keyword in ["current", "i/a"]):
            output_lines.append(line)
            continue
        if any(keyword in parts[1].lower() for keyword in ["flux", "b/mt"]):
            output_lines.append(line)
            continue
        
        # Try to negate numeric values
        try:
            current = float(parts[0])
            flux = float(parts[1])
            negated_current = -current
            negated_flux = -flux
            output_lines.append(f"{negated_current:.3f}\t{negated_flux:.3f}\n")
        except ValueError:
            # If not numeric, keep original
            output_lines.append(line)
    
    # Write back to file
    with DATA_FILE.open("w", encoding="utf-8") as f:
        f.writelines(output_lines)
    
    print(f"Successfully negated all readings in {DATA_FILE.name}")

if __name__ == "__main__":
    negate_dataset()
