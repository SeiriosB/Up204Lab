import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ----------------------------------------------------------------------------
# Pressure Sensor Calibration: Pressure vs Voltage
# Data from experimental table
# ----------------------------------------------------------------------------

# Voltage in mV
voltage = np.array([-0.85, 3.30, 7.87, 12.70, 18.00, 26.10, 31.20, 37.60, 
                    46.20, 54.80, 64.30, 75.20, 87.20, 102.50])

# Pressure in atm
pressure = np.array([1.0000, 1.0364, 1.0756, 1.1179, 1.1636, 1.2132, 1.2673, 
                     1.3263, 1.3912, 1.4627, 1.5420, 1.6304, 1.7295, 1.8414])

# Perform linear regression
slope, intercept, r_val, p_val, std_err = linregress(voltage, pressure)
r_squared = r_val**2

# Calculate intercept standard error
n = len(voltage)
x_mean = np.mean(voltage)
s_x = np.sum((voltage - x_mean)**2)
intercept_stderr = std_err * np.sqrt(np.sum(voltage**2) / n)

# Print results
print("="*70)
print("PRESSURE SENSOR CALIBRATION: Pressure vs Voltage")
print("="*70)
print(f"Linear Fit: P = {intercept:.6f} + {slope:.6e}*V")
print(f"Slope = {slope:.6e} ± {std_err:.6e} atm/mV")
print(f"Intercept = {intercept:.6f} ± {intercept_stderr:.6f} atm")
print(f"R² = {r_squared:.6f}")
print("="*70)
print()

# Create the plot
plt.figure(figsize=(10, 7))

# Plot data points
plt.scatter(voltage, pressure, color='darkblue', s=100, label='Experimental Data', 
            zorder=3, edgecolors='black', linewidth=1.5)

# Plot linear fit
V_fit = np.linspace(min(voltage), max(voltage), 500)
P_fit = slope * V_fit + intercept
plt.plot(V_fit, P_fit, 'r-', linewidth=2, 
         label=f'Linear Fit: $P = {intercept:.4f} + (8.196 \\times 10^{{-3}})V$\n$R^2 = {r_squared:.6f}$')

# Labels and formatting
plt.xlabel('Voltage (mV)', fontsize=14, fontweight='bold')
plt.ylabel('Pressure (atm)', fontsize=14, fontweight='bold')
plt.title('Pressure Sensor Calibration Curve', fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='lower right')
plt.minorticks_on()
plt.grid(True, which='major', linestyle='--', alpha=0.5, linewidth=0.7)
plt.grid(True, which='minor', linestyle=':', alpha=0.3, linewidth=0.5)
plt.tight_layout()

# Save the figure
plt.savefig('pressure_calibration.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'pressure_calibration.png'")
plt.show()