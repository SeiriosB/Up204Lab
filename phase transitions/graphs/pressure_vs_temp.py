import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Phase Transition: Pressure vs Temperature
# Data from Table 2
# ----------------------------------------------------------------------------

# Temperature in Celsius
temperature = np.array([25.1, 30.0, 35.0, 40.1, 45.0, 50.0, 55.0, 60.0, 65.0, 70.1])

# Pressure in atm
pressure = np.array([1.0085, 1.0184, 1.0381, 1.0602, 1.0864, 1.1160, 1.1512, 1.1963, 1.2488, 1.3111])

# Print data info
print("="*70)
print("PHASE TRANSITION: Total Pressure vs Temperature")
print("="*70)
print(f"Temperature range: {temperature.min():.1f} - {temperature.max():.1f} °C")
print(f"Pressure range: {pressure.min():.4f} - {pressure.max():.4f} atm")
print("="*70)
print()

# Create the plot
plt.figure(figsize=(10, 7))

# Plot data points with connecting line
plt.plot(temperature, pressure, 'o-', color='darkred', linewidth=2, markersize=8, 
         markeredgecolor='black', markeredgewidth=1.5, label='Experimental Data')

# Labels and formatting
plt.xlabel('Temperature (°C)', fontsize=14, fontweight='bold')
plt.ylabel('Total Pressure (atm)', fontsize=14, fontweight='bold')
plt.title('Total Pressure versus Temperature', fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='lower right')

# Set x-axis major ticks at 10°C intervals
from matplotlib.ticker import MultipleLocator
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(2))

plt.minorticks_on()
plt.grid(True, which='major', linestyle='--', alpha=0.5, linewidth=0.7)
plt.grid(True, which='minor', linestyle=':', alpha=0.3, linewidth=0.5)
plt.tight_layout()

# Save the figure
plt.savefig('pressure_vs_temperature.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'pressure_vs_temperature.png'")
plt.show()
