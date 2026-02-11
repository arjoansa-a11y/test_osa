import numpy as np 
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

def dBmtoW(P_dBm):
    return 10**(P_dBm/10)*1E-3  

def plot_trace(trace):
    w = trace[0]
    p = trace[1]
    plt.figure(1)
    plt.plot(w, p)
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Power [dBm]')
    plt.show()

def WtodBm(P_W):
    # Convert lists or scalars to numpy array for uniform handling
    P_W = np.asarray(P_W)

    # Check for non-positive values
    if np.any(P_W <= 0):
        raise ValueError("Power in watts must be positive and non-zero")

    # Compute dBm
    return 10 * np.log10(P_W * 1e3)