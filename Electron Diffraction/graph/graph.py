import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Data from Table 2 (Determination of d_2)
sin_theta_2 = np.array([0.1027, 0.0988, 0.0882, 0.0853, 0.0757, 0.0743, 0.0705])
lambda_theo = np.array([0.274, 0.245, 0.224, 0.207, 0.194, 0.183, 0.173])  # Angstroms
lambda_exp = np.array([0.265, 0.239, 0.212, 0.197, 0.186, 0.179, 0.172])  # Angstroms

# ============================================================================
# First Plot: lambda_theo vs sin(theta_2)
# ============================================================================

print("="*80)
print("First Plot: lambda_theo vs sin(theta_2)")
print("="*80)

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(sin_theta_2, lambda_theo)

# Calculate 2*d_2 from slope
d_2 = slope / 2
d_2_error = std_err / 2

print("\nLinear Regression Results:")
print(f"Slope (2*d_2): {slope:.4f} ± {std_err:.4f} Å")
print(f"Intercept: {intercept:.6f}")
print(f"R-squared: {r_value**2:.4f}")
print(f"\nInter-planar distance:")
print(f"d_2 = {d_2:.4f} ± {d_2_error:.4f} Å")

# Generate fitted line
sin_theta_2_fit = np.linspace(sin_theta_2.min(), sin_theta_2.max(), 100)
lambda_theo_fit = slope * sin_theta_2_fit + intercept

# Create the plot
plt.figure(figsize=(10, 7))
plt.scatter(sin_theta_2, lambda_theo, s=20, color='black', marker='o', zorder=3)
plt.plot(sin_theta_2_fit, lambda_theo_fit, 'r-', linewidth=2, 
         label=f'y = ({slope:.4f} ± {std_err:.4f})x + ({intercept:.6f})\nR² = {r_value**2:.4f}', 
         zorder=2)

# Add finer grid
plt.grid(True, alpha=0.3, linestyle='--', which='both')
plt.minorticks_on()
plt.grid(True, which='minor', alpha=0.15, linestyle=':')

# Labels and title
plt.xlabel(r'$\sin(\theta_2)$', fontsize=14)
plt.ylabel(r'$\lambda_{theo}$ (Å)', fontsize=14, rotation=0, labelpad=20)
plt.title(r'$\lambda_{theo}$ vs $\sin(\theta_2)$', fontsize=16)
plt.legend(fontsize=11, loc='upper left')

plt.tight_layout()

# Save the figure
output_path = '/home/Animesh/phys_lab_sem4/up204/Electron Diffraction/graph/lambda_theo_plot.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\nPlot saved to: {output_path}")



# ============================================================================
# Second Plot: lambda_exp vs sin(theta_2)
# ============================================================================

print("\n" + "="*80)
print("Second Plot: lambda_exp vs sin(theta_2)")
print("="*80)

# Perform linear regression
slope2, intercept2, r_value2, p_value2, std_err2 = linregress(sin_theta_2, lambda_exp)

# Calculate 2*d_2 from slope
d_2_exp = slope2 / 2
d_2_exp_error = std_err2 / 2

print("\nLinear Regression Results:")
print(f"Slope (2*d_2): {slope2:.4f} ± {std_err2:.4f} Å")
print(f"Intercept: {intercept2:.6f}")
print(f"R-squared: {r_value2**2:.4f}")
print(f"\nInter-planar distance:")
print(f"d_2 = {d_2_exp:.4f} ± {d_2_exp_error:.4f} Å")

# Generate fitted line
lambda_exp_fit = slope2 * sin_theta_2_fit + intercept2

# Create the plot
plt.figure(figsize=(10, 7))
plt.scatter(sin_theta_2, lambda_exp, s=20, color='black', marker='o', zorder=3)
plt.plot(sin_theta_2_fit, lambda_exp_fit, 'r-', linewidth=2, 
         label=f'y = ({slope2:.4f} ± {std_err2:.4f})x + ({intercept2:.6f})\nR² = {r_value2**2:.4f}', 
         zorder=2)

# Add finer grid
plt.grid(True, alpha=0.3, linestyle='--', which='both')
plt.minorticks_on()
plt.grid(True, which='minor', alpha=0.15, linestyle=':')

# Labels and title
plt.xlabel(r'$\sin(\theta_2)$', fontsize=14)
plt.ylabel(r'$\lambda_{exp}$ (Å)', fontsize=14, rotation=0, labelpad=20)
plt.title(r'$\lambda_{exp}$ vs $\sin(\theta_2)$', fontsize=16)
plt.legend(fontsize=11, loc='upper left')

plt.tight_layout()

# Save the figure
output_path2 = '/home/Animesh/phys_lab_sem4/up204/Electron Diffraction/graph/lambda_exp_plot.png'
plt.savefig(output_path2, dpi=300, bbox_inches='tight')
print(f"\nPlot saved to: {output_path2}")


