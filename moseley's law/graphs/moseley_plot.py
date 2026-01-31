import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Data from the table: Z, theta, lambda, sqrt(E)
# Zn (30): 18.4°, 127.1 pm, 98.8 eV^(1/2)
# Sr (38): 10.7°, 74.8 pm, 128.8 eV^(1/2)
# Ag (47): 6.8°, 47.7 pm, 161.3 eV^(1/2)

Z = np.array([30, 38, 47])  # Atomic numbers
sqrt_E = np.array([98.8, 128.8, 161.3])  # sqrt(E) in eV^(1/2)

# Perform linear regression
slope, intercept, r_val, p_val, std_err_slope = linregress(Z, sqrt_E)

# Calculate standard error of intercept
n = len(Z)
residuals = sqrt_E - (slope * Z + intercept)
std_residual = np.sqrt(np.sum(residuals**2) / (n - 2))
Z_mean = np.mean(Z)
std_err_intercept = std_residual * np.sqrt(1/n + Z_mean**2 / np.sum((Z - Z_mean)**2))

# Calculate uncertainties in derived quantities
# For Rhc = slope^2
Rhc = slope**2
delta_Rhc = 2 * slope * std_err_slope

# For Rydberg constant R = Rhc / (hc)
h = 4.136e-15  # eV·s
c = 3.0e8  # m/s
hc = h * c
R = Rhc / hc
delta_R = delta_Rhc / hc

# For screening constant sigma = -intercept / slope
sigma = -intercept / slope
delta_sigma = sigma * np.sqrt((std_err_intercept/intercept)**2 + (std_err_slope/slope)**2)

print("="*60)
print("MOSELEY'S LAW: sqrt(E) vs Z")
print("="*60)
print(f"Linear Fit: sqrt(E) = ({slope:.4f} ± {std_err_slope:.4f}) * Z + ({intercept:.2f} ± {std_err_intercept:.2f})")
print(f"R² = {r_val**2:.6f}")
print()
print(f"Rhc = {Rhc:.3f} ± {delta_Rhc:.3f} eV")
print(f"Rydberg constant R = ({R:.3e} ± {delta_R:.3e}) m^(-1)")
print(f"Screening constant σ = {sigma:.3f} ± {delta_sigma:.3f}")
print()

# Create the plot
plt.figure(figsize=(10, 7))
plt.scatter(Z, sqrt_E, color='darkblue', s=100, label='Experimental Data', 
            zorder=3, edgecolors='black', linewidth=2)
plt.plot(Z, slope*Z + intercept, 'r-', linewidth=2,
         label=f'$\\sqrt{{E}}$ = ({slope:.3f} ± {std_err_slope:.3f})$Z$ + ({intercept:.1f} ± {std_err_intercept:.1f})\n$R^2$ = {r_val**2:.6f}')

plt.xlabel('Atomic Number (Z)', fontsize=14, fontweight='bold')
plt.ylabel('$\\sqrt{E}$ (eV$^{1/2}$)', fontsize=14, fontweight='bold')
plt.title("Moseley's Law: $\\sqrt{E}$ vs Z", fontsize=16, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5, linewidth=0.7)
plt.tight_layout()
plt.savefig('moseley_law_plot.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'moseley_law_plot.png'")

# Use the fit to predict Z for unknown sample with uncertainty
unknown_sqrt_E = 134.5
predicted_Z = (unknown_sqrt_E - intercept) / slope
# Uncertainty in predicted Z (assuming negligible uncertainty in unknown_sqrt_E measurement)
delta_Z = predicted_Z * np.sqrt((std_err_intercept/intercept)**2 + (std_err_slope/slope)**2)
print(f"\nPredicted Z for Unknown sample: {predicted_Z:.1f} ± {delta_Z:.1f}")
print("="*60)
