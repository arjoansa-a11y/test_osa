import numpy as np 
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import os
from os.path import isfile, expanduser

def save_trace(folder_measurements,file_name, yaml, osa, data):
    yaml.osa_idn = osa.id
    yaml.osa_resolution = osa.resolution_bandwidth
    yaml.osa_sensitivity = osa.sensitivity_level
    yaml.osa_start_wavelength = osa.wavelength_center-osa.wavelength_span/2
    yaml.osa_stop_wavelength =  osa.wavelength_center+osa.wavelength_span/2
    yaml.osa_sweep_mode = osa.sweep_mode
    yaml.osa_integrated_power = osa.integrated_power
    yaml.osa_dBm_nm = osa.dBm_nm
    os.makedirs(folder_measurements, exist_ok=True)
    filename = '\\'.join([folder_measurements,file_name])
    header = '\n'.join([' ' + str(a) + ': ' + str(b) for a, b in yaml.__dict__.items()])
    if osa.dBm_nm:
        header = header + '\n\n' + ' Wavelength [nm] \t Power [dBm/nm]'
    else:
        header = header + '\n\n' + ' Wavelength [nm] \t Power [dBm]'
    if isfile(filename + '.txt'):
        i = 0
        filename = filename + '_copy' + str(i)
        while isfile(filename+'.txt'):
            i = i+1
            filename = filename[:-1] + str(i)
    np.savetxt(filename + '.txt', [list(i) for i in zip(*data)], fmt='%2.10f', delimiter='\t', header=header,
                comments='%')


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