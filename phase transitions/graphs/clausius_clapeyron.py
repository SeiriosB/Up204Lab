import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ----------------------------------------------------------------------------
# Clausius-Clapeyron Plot: ln(P_vapor) vs 1/T
# Data from Table 4
# ----------------------------------------------------------------------------

# 1/T in K^-1
inv_T = np.array([0.003353, 0.003299, 0.003245, 0.003192, 0.003143, 
                  0.003095, 0.003047, 0.003002, 0.002957, 0.002913])

# ln(P_vapor)
ln_P_vapor = np.array([-4.2545, -4.8030, -4.4478, -4.0571, -3.5860, 
                       -3.1916, -2.8098, -2.4167, -2.0740, -1.7630])

# Perform linear regression
slope, intercept, r_val, p_val, std_err = linregress(inv_T, ln_P_vapor)
r_squared = r_val**2

# Calculate intercept standard error
n = len(inv_T)
intercept_stderr = std_err * np.sqrt(np.sum(inv_T**2) / n)

# Print results
print("="*70)
print("CLAUSIUS-CLAPEYRON PLOT: ln(P_vapor) vs 1/T")
print("="*70)
print(f"Linear Fit: ln(P) = {intercept:.4f} + {slope:.4f}*(1/T)")
print(f"Slope = {slope:.4f} ± {std_err:.4f} K")
print(f"Intercept = {intercept:.4f} ± {intercept_stderr:.4f}")
print(f"R² = {r_squared:.6f}")
print(f"\nLatent Heat (from slope): ΔH_vap = -R × slope = {-slope * 8.314:.2f} J/mol")
print("="*70)
print()

# Create the plot
plt.figure(figsize=(10, 7))

# Plot data points
plt.scatter(inv_T, ln_P_vapor, color='darkviolet', s=100, label='Experimental Data', 
            zorder=3, edgecolors='black', linewidth=1.5)

# Plot linear fit
inv_T_fit = np.linspace(min(inv_T), max(inv_T), 500)
ln_P_fit = slope * inv_T_fit + intercept
plt.plot(inv_T_fit, ln_P_fit, 'r-', linewidth=2, 
         label=f'Linear Fit: $\\ln(P) = {intercept:.2f} + ({slope:.0f})(1/T)$\n$R^2 = {r_squared:.6f}$')

# Labels and formatting
plt.xlabel('$1/T$ (K$^{-1}$)', fontsize=14, fontweight='bold')
plt.ylabel('$\\ln(P_{\\mathrm{vapor}})$', fontsize=14, fontweight='bold')
plt.title('Clausius-Clapeyron Plot', fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='upper right')
plt.minorticks_on()
plt.grid(True, which='major', linestyle='--', alpha=0.5, linewidth=0.7)
plt.grid(True, which='minor', linestyle=':', alpha=0.3, linewidth=0.5)
plt.tight_layout()

# Save the figure
plt.savefig('clausius_clapeyron.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'clausius_clapeyron.png'")
plt.show()
