import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Vapor Pressure vs Temperature
# Data from Table 3
# ----------------------------------------------------------------------------

# Temperature in Celsius
temperature = np.array([25.1, 30.0, 35.0, 40.1, 45.0, 50.0, 55.0, 60.0, 65.0, 70.1])

# Vapor Pressure in atm
vapor_pressure = np.array([0.0142, 0.0082, 0.0117, 0.0173, 0.0277, 0.0411, 0.0602, 0.0892, 0.1256, 0.1714])

# Print data info
print("="*70)
print("Vapor Pressure vs Temperature")
print("="*70)
print(f"Temperature range: {temperature.min():.1f} - {temperature.max():.1f} °C")
print(f"Vapor Pressure range: {vapor_pressure.min():.4f} - {vapor_pressure.max():.4f} atm")
print("="*70)
print()

# Create the plot
plt.figure(figsize=(10, 7))

# Plot data points with connecting line
plt.plot(temperature, vapor_pressure, 'o-', color='darkgreen', linewidth=2, markersize=8, 
         markeredgecolor='black', markeredgewidth=1.5, label='Experimental Data')

# Labels and formatting
plt.xlabel('Temperature (°C)', fontsize=14, fontweight='bold')
plt.ylabel('Vapor Pressure (atm)', fontsize=14, fontweight='bold')
plt.title('Vapor Pressure versus Temperature', fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='upper left')

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
plt.savefig('vapor_pressure_vs_temperature.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'vapor_pressure_vs_temperature.png'")
plt.show()
