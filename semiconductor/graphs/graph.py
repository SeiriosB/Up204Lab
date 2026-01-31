import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. DATA LOADER FUNCTION
# ==========================================
def load_data(filename):
    """
    Reads data from files skipping headers.
    Assumes columns: Voltage(mV), Current(mA), ...
    """
    try:
        # Load numeric data, skipping header rows automatically
        data = np.genfromtxt(filename, skip_header=3) 
        
        if data.ndim == 1:
             return None, None
             
        voltage_mv = data[:, 0]
        current_ma = data[:, 1]
        
        return voltage_mv, current_ma
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return np.array([]), np.array([])

# ==========================================
# 2. ANALYSIS FUNCTIONS
# ==========================================
def get_knee_voltage(v, i, target_i=1.0):
    """Finds voltage where current crosses target_i (default 1mA)"""
    if len(i) == 0: return 0
    idx = (np.abs(i - target_i)).argmin()
    return v[idx]

def get_ideality_factor_from_mask(v_mv, i_ma, mask, temp_k=298):
    """
    Calculates ideality factor n from slope of ln(I) vs V using a specific subset of data.
    """
    if np.sum(mask) < 2: 
        return 0, 0, 0
    
    v_fit = v_mv[mask] / 1000.0 # Convert to Volts
    i_fit = np.log(i_ma[mask])  # ln(Current)
    
    # Linear Fit
    slope, intercept = np.polyfit(v_fit, i_fit, 1)
    
    # Constants
    q = 1.602e-19
    k = 1.38e-23
    
    if slope == 0: return 0, 0, 0
    
    eta = q / (slope * k * temp_k)
    return eta, slope, intercept

# ==========================================
# 3. MAIN PROCESSING
# ==========================================

# Current Script Directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data Directory
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

# Graphs Output Directory
GRAPHS_DIR = SCRIPT_DIR

diode_files = {
    'irled1': 'IR LED',
    'uvled': 'UV LED',
    'redled': 'Red LED',
    'greled': 'Green LED',
    'bluled': 'Blue LED',
    'yelled': 'Yellow LED',
    '1N4007for': '1N4007 Diode',
    '1N4148for': '1N4148 Diode',
    'beivch': 'Transistor B-E',
    'bcivch': 'Transistor B-C',
}

transistor_files = {
    '020Ic': 'Ib = 20 uA',
    '040Ic': 'Ib = 40 uA',
    '060Ic': 'Ib = 60 uA',
    '080Ic': 'Ib = 80 uA'
}

# --- CUSTOM VOLTAGE RANGES (mV) for Semi-Log Plots ---
custom_cutoffs = {
    '1N4007for': 600,
    '1N4148for': 600,
    'beivch': 750,
    'bcivch': 750,
    'irled1': 1250,
    'redled': None,  # None = Entire range
    'greled': 500,
    'bluled': 900,
    'yelled': 900,   # Fallback
    'uvled': 9300
}

print(f"Reading data from: {DATA_DIR}")
print(f"Saving graphs to: {GRAPHS_DIR}")

if os.path.exists(DATA_DIR):
    all_files = sorted(os.listdir(DATA_DIR))
    
    for fname in all_files:
        file_path = os.path.join(DATA_DIR, fname)
        
        if os.path.isdir(file_path): continue
            
        v, i = load_data(file_path)
        
        if v is None or len(v) == 0:
            print(f"Skipping empty or invalid file: {fname}")
            continue

        # ==========================================
        # DIODES & TRANSISTOR JUNCTIONS
        # ==========================================
        if fname in diode_files:
            label = diode_files[fname]
            
            # Calculate knee voltage
            knee_v = get_knee_voltage(v, i, target_i=1.0)
            print(f"{label}: Knee Voltage = {knee_v:.2f} mV")
            
            # --- PLOT 1: STANDARD I-V CURVE (Linear Scale) ---
            plt.figure(figsize=(8, 6))
            plt.plot(v, i, 'o-', markersize=4, label=label, color='blue')
            plt.title(f"{label} I-V Characteristic")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Current (mA)")
            plt.grid(True)
            plt.legend()
            
            save_path_lin = os.path.join(GRAPHS_DIR, fname + ".png")
            plt.savefig(save_path_lin)
            plt.close()
            print(f"Saved: {save_path_lin}")

            # --- DETERMINE MASK FOR SEMI-LOG PLOT ---
            cutoff = custom_cutoffs.get(fname, 0)
            
            if cutoff is None: 
                 mask = (i > 0.001)
            else:
                 mask = (v > cutoff) & (i > 0.001)
            
            # --- PLOT 2: SEMI-LOG PLOT (Masked Data Only) ---
            v_log = v[mask]
            i_log = i[mask]

            if len(v_log) > 0:
                plt.figure(figsize=(8, 6))
                
                # Plot Data Points (label starts with _ to exclude from legend)
                plt.semilogy(v_log, i_log, 'o', markersize=4, color='red', label='_Data')
                
                # --- CALCULATE & PLOT BEST FIT ---
                # Fit ln(I) vs V (mV) to get nice equation in terms of mV
                # y = ln(I) = m*x + c  =>  I = e^(m*x + c)
                
                v_fit_mv = v_log
                i_fit_ln = np.log(i_log)
                
                slope_mv, intercept_ln = np.polyfit(v_fit_mv, i_fit_ln, 1)
                
                # Generate fit line
                fit_line_y = np.exp(slope_mv * v_fit_mv + intercept_ln)
                
                # Create Equation String for Legend
                # ln(I) = m*V + c
                equation_str = f"ln(I) = {slope_mv:.4f}V + {intercept_ln:.2f}"
                
                # Calculate ideality factor
                q = 1.602e-19
                k = 1.38e-23
                temp_k = 298
                # slope_mv is in units of 1/mV, convert to 1/V
                slope_v = slope_mv * 1000  # slope per Volt
                eta = q / (slope_v * k * temp_k)
                
                print(f"{label}: Slope = {slope_mv:.4f} mV^-1, Ideality Factor = {eta:.2f}")
                
                plt.semilogy(v_fit_mv, fit_line_y, '-', color='black', linewidth=1.5, label=equation_str)

                plt.title(f"{label} Semi-Log Plot")
                plt.xlabel("Voltage (mV)")
                plt.ylabel("Current (mA) - Log Scale")
                plt.grid(True, which="both", ls="-", alpha=0.5)
                plt.legend() # Only fit line should appear
                
                save_path_log = os.path.join(GRAPHS_DIR, fname + "_log.png")
                plt.savefig(save_path_log)
                plt.close()
                print(f"Saved: {save_path_log}")
            else:
                print(f"No data points for semi-log plot for {fname} (cutoff: {cutoff} mV)")

        # ==========================================
        # TRANSISTOR OUTPUT CHARACTERISTICS
        # ==========================================
        elif fname in transistor_files:
            label = transistor_files[fname]
            
            plt.figure(figsize=(8, 6))
            plt.plot(v, i, 'o-', markersize=4, label=label, color='green')
            plt.title(f"Output Characteristic {label}")
            plt.xlabel("Voltage Vce (mV)")
            plt.ylabel("Current Ic (mA)")
            plt.grid(True)
            plt.legend()
            
            save_path_trans = os.path.join(GRAPHS_DIR, fname + ".png")
            plt.savefig(save_path_trans)
            plt.close()
            print(f"Saved: {save_path_trans}")
