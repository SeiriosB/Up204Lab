import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ----------------------------------------------------------------------------
# Table 1: Determination of Wire Thickness (a₁) for Single Helix
# Plot: x_n (Mean) vs n (Order)
# ----------------------------------------------------------------------------
# Order n
n = np.array([1, 2, 3, 4, 5, 6, 7])
# Mean x_n values in cm
x_n = np.array([1.27, 2.40, 3.49, 4.71, 5.91, 7.13, 8.30])

# Perform linear regression
slope_1, intercept_1, r_val_1, p_val_1, std_err_1 = linregress(n, x_n)

print("="*60)
print("TABLE 1: Wire Thickness Determination")
print("="*60)
print(f"Linear Fit: x_n = ({slope_1:.4f} ± {std_err_1:.4f}) * n + ({intercept_1:.4f})")
print(f"R² = {r_val_1**2:.6f}")
print()

# Create the plot for Table 1
plt.figure(figsize=(10, 7))
plt.scatter(n, x_n, color='darkblue', s=80, label='Experimental Data', zorder=3, edgecolors='black', linewidth=1.5)
plt.plot(n, slope_1*n + intercept_1, 'r-', linewidth=2,
         label=f'Linear Fit: $x_n$ = {slope_1:.3f}$n$ + {intercept_1:.3f}\n$R^2$ = {r_val_1**2:.6f}')

plt.xlabel('Order ($n$)', fontsize=14, fontweight='bold')
plt.ylabel('Mean Position $x_n$ (cm)', fontsize=14, fontweight='bold')
plt.title('Table 1: Determination of Wire Thickness ($a_1$)', fontsize=16, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5, linewidth=0.7)
plt.tight_layout()
plt.savefig('table1_xn_vs_n.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'table1_xn_vs_n.png'\n")

# ----------------------------------------------------------------------------
# Table 2: Determination of Turn Separation (d₁) for Single Helix
# Plot: x_m (Average) vs m (Order)
# ----------------------------------------------------------------------------
# Order m (excluding minima gaps)
m = np.array([1, 2, 3, 4, 7, 8, 9, 10, 14, 15, 16, 19, 20, 21, 24, 25, 26, 27, 30, 31, 32])
# Average x_m values in cm
x_m = np.array([0.20, 0.45, 0.65, 0.85, 1.50, 1.70, 1.90, 2.10, 2.90, 3.10, 3.30, 
                3.95, 4.15, 4.30, 5.00, 5.20, 5.40, 5.60, 6.35, 6.55, 6.75])

# Perform linear regression
slope_2, intercept_2, r_val_2, p_val_2, std_err_2 = linregress(m, x_m)

print("="*60)
print("TABLE 2: Turn Separation Determination")
print("="*60)
print(f"Linear Fit: x_m = ({slope_2:.6f} ± {std_err_2:.6f}) * m + ({intercept_2:.4f})")
print(f"R² = {r_val_2**2:.6f}")
print()

# Create the plot for Table 2
plt.figure(figsize=(12, 7))
plt.scatter(m, x_m, color='darkgreen', s=80, label='Experimental Data', zorder=3, edgecolors='black', linewidth=1.5)
plt.plot(m, slope_2*m + intercept_2, 'r-', linewidth=2,
         label=f'Linear Fit: $x_m$ = {slope_2:.5f}$m$ + {intercept_2:.3f}\n$R^2$ = {r_val_2**2:.6f}')

plt.xlabel('Order ($m$)', fontsize=14, fontweight='bold')
plt.ylabel('Average Position $x_m$ (cm)', fontsize=14, fontweight='bold')
plt.title('Table 2: Determination of Turn Separation ($d_1$)', fontsize=16, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5, linewidth=0.7)
plt.tight_layout()
plt.savefig('table2_xm_vs_m.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'table2_xm_vs_m.png'\n")

# ----------------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------------
print("="*60)
print("SUMMARY OF LINEAR FITS")
print("="*60)
print(f"Table 1 (x_n vs n): Slope = {slope_1:.4f} ± {std_err_1:.4f} cm, R² = {r_val_1**2:.6f}")
print(f"Table 2 (x_m vs m): Slope = {slope_2:.6f} ± {std_err_2:.6f} cm, R² = {r_val_2**2:.6f}")
print("="*60)

# ----------------------------------------------------------------------------
# Table 3: Pitch and Turn Spacing Determination for Double Helix
# Plot: x_n (Average) vs n (Order)
# ----------------------------------------------------------------------------
# Order n
n_double = np.array([1, 2, 3, 4])
# Average x_n values in cm
x_n_double = np.array([3.83, 7.58, 11.68, 15.53])

# Perform linear regression
slope_3, intercept_3, r_val_3, p_val_3, std_err_3 = linregress(n_double, x_n_double)

print("\n" + "="*60)
print("TABLE 3: Helix Thickness Determination (a₂) - Double Helix")
print("="*60)
print(f"Linear Fit: x_n = ({slope_3:.4f} ± {std_err_3:.4f}) * n + ({intercept_3:.4f})")
print(f"R² = {r_val_3**2:.6f}")
print()

# Create the plot for Table 3
plt.figure(figsize=(10, 7))
plt.scatter(n_double, x_n_double, color='purple', s=100, label='Experimental Data', zorder=3, edgecolors='black', linewidth=1.5)
plt.plot(n_double, slope_3*n_double + intercept_3, 'r-', linewidth=2,
         label=f'Linear Fit: $x_n$ = {slope_3:.3f}$n$ + {intercept_3:.3f}\n$R^2$ = {r_val_3**2:.6f}')

plt.xlabel('Order ($n$)', fontsize=14, fontweight='bold')
plt.ylabel('Average Position $x_n$ (cm)', fontsize=14, fontweight='bold')
plt.title('Table 3: Helix Thickness ($a_2$) - Double Helix', fontsize=16, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5, linewidth=0.7)
plt.tight_layout()
plt.savefig('table3_double_helix_thickness.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'table3_double_helix_thickness.png'\n")

# ----------------------------------------------------------------------------
# Table 4: Helix Separation Determination (S) - Double Helix
# Plot: x_m (Mean) vs m (Order)
# ----------------------------------------------------------------------------
# Order m (excluding missing orders)
m_double = np.array([2, 3, 4, 7, 8, 9, 13, 14, 15, 19, 20])
# Mean x_m values in cm
x_m_double = np.array([1.50, 2.10, 2.80, 5.00, 5.75, 6.50, 8.90, 9.60, 10.50, 13.30, 13.80])

# Perform linear regression
slope_4, intercept_4, r_val_4, p_val_4, std_err_4 = linregress(m_double, x_m_double)

print("="*60)
print("TABLE 4: Helix Separation Determination (S) - Double Helix")
print("="*60)
print(f"Linear Fit: x_m = ({slope_4:.6f} ± {std_err_4:.6f}) * m + ({intercept_4:.4f})")
print(f"R² = {r_val_4**2:.6f}")
print()

# Create the plot for Table 4
plt.figure(figsize=(12, 7))
plt.scatter(m_double, x_m_double, color='darkorange', s=80, label='Experimental Data', zorder=3, edgecolors='black', linewidth=1.5)
plt.plot(m_double, slope_4*m_double + intercept_4, 'r-', linewidth=2,
         label=f'Linear Fit: $x_m$ = {slope_4:.5f}$m$ + {intercept_4:.3f}\n$R^2$ = {r_val_4**2:.6f}')

plt.xlabel('Order ($m$)', fontsize=14, fontweight='bold')
plt.ylabel('Mean Position $x_m$ (cm)', fontsize=14, fontweight='bold')
plt.title('Table 4: Helix Separation ($S$) - Double Helix', fontsize=16, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5, linewidth=0.7)
plt.tight_layout()
plt.savefig('table4_double_helix_separation.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'table4_double_helix_separation.png'\n")

# ----------------------------------------------------------------------------
# Table 5: Turn Separation Determination (d₂) - Double Helix
# Plot: x_ℓ (Distance) vs ℓ (Order)
# ----------------------------------------------------------------------------
# Order ℓ (excluding missing orders)
l_double = np.array([1, 2, 3, 4, 7, 9, 10, 13, 14, 19, 20, 23, 24, 27, 28, 31, 32, 37, 38, 41, 42, 43, 46, 47, 48, 49, 55, 56, 59, 60, 61])
# Distance x_ℓ values in cm
x_l_double = np.array([0.7, 0.9, 1.0, 1.2, 1.8, 2.3, 2.5, 3.0, 3.1, 4.5, 4.7, 5.2, 5.4, 6.0, 6.2, 6.8, 7.0, 8.3, 8.5, 9.2, 9.4, 9.9, 10.4, 10.8, 11.0, 11.2, 12.6, 12.8, 13.4, 14.0, 14.2])

# Perform linear regression
slope_5, intercept_5, r_val_5, p_val_5, std_err_5 = linregress(l_double, x_l_double)

print("="*60)
print("TABLE 5: Turn Separation Determination (d₂) - Double Helix")
print("="*60)
print(f"Linear Fit: x_ℓ = ({slope_5:.6f} ± {std_err_5:.6f}) * ℓ + ({intercept_5:.4f})")
print(f"R² = {r_val_5**2:.6f}")
print()

# Create the plot for Table 5
plt.figure(figsize=(12, 8))
plt.scatter(l_double, x_l_double, color='teal', s=60, label='Experimental Data', zorder=3, edgecolors='black', linewidth=1.2)
plt.plot(l_double, slope_5*l_double + intercept_5, 'r-', linewidth=2,
         label=f'Linear Fit: $x_\\ell$ = {slope_5:.5f}$\\ell$ + {intercept_5:.3f}\n$R^2$ = {r_val_5**2:.6f}')

plt.xlabel('Order ($\\ell$)', fontsize=14, fontweight='bold')
plt.ylabel('Distance $x_\\ell$ (cm)', fontsize=14, fontweight='bold')
plt.title('Table 5: Turn Separation ($d_2$) - Double Helix', fontsize=16, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5, linewidth=0.7)
plt.tight_layout()
plt.savefig('table5_double_helix_turn_separation.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as 'table5_double_helix_turn_separation.png'\n")

# ----------------------------------------------------------------------------
# Final Summary
# ----------------------------------------------------------------------------
print("\n" + "="*60)
print("COMPLETE SUMMARY OF ALL LINEAR FITS")
print("="*60)
print("SINGLE HELIX:")
print(f"  Table 1 (Wire thickness a₁): Slope = {slope_1:.4f} ± {std_err_1:.4f} cm, R² = {r_val_1**2:.6f}")
print(f"  Table 2 (Turn separation d₁): Slope = {slope_2:.6f} ± {std_err_2:.6f} cm, R² = {r_val_2**2:.6f}")
print("\nDOUBLE HELIX:")
print(f"  Table 3 (Helix thickness a₂): Slope = {slope_3:.4f} ± {std_err_3:.4f} cm, R² = {r_val_3**2:.6f}")
print(f"  Table 4 (Helix separation S): Slope = {slope_4:.6f} ± {std_err_4:.6f} cm, R² = {r_val_4**2:.6f}")
print(f"  Table 5 (Turn separation d₂): Slope = {slope_5:.6f} ± {std_err_5:.6f} cm, R² = {r_val_5**2:.6f}")
print("="*60)