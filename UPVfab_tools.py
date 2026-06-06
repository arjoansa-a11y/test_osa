import numpy as np
import ast
from scipy.signal import find_peaks

def open_file(file_path, print_header=False):
    """Function to open OSA data file, extract header information and load wavelength and power data.

    Inputs:
    - file_path: path to the OSA data file
    - print_header: boolean to indicate whether to print header information (default: False)

    Outputs:
    - wavelength: array of wavelength values
    - power: array of power values (adjusted for splitter loss)

    Notes:
    - The function assumes that the splitter header information is in the format "1x2-50/50" (input x output - OSA/OPM) and calculates the
    splitter loss accordingly. If the splitter is "na", it assumes no splitter loss."""

    # Open file
    with open(file_path, 'r') as f:
        first_line = f.readline()

    # Obtain header information 
    header_str = first_line[first_line.find("{"):].strip() 
    header_dict = ast.literal_eval(header_str)
    
    # Print header information
    if print_header:
        print("#"*90)
        print("FILE DATA:")
        print("#"*90)
        for key, value in header_dict.items():
            print(f"{key}: {value}")

    # Calculate splitter loss and adjustment power values
    if header_dict['splitter'] == 'na':
        splitter_opm_loss = 0
        splitter_osa_loss = 0
    
    # For a format like "1x2-50/50" (input x output - OSA/OPM)
    else:
        splitter_loss = header_dict['splitter'].split('-')[-1].split('/')
        splitter_opm_loss = 10*np.log10(float(splitter_loss[1])/100)
        splitter_osa_loss = 10*np.log10(float(splitter_loss[0])/100)

    # Load wavelength and power data
    wavelength, power = np.loadtxt(file_path, comments='%', unpack=True)
    wavelength = wavelength.astype('float')
    power = power.astype('float')

    return wavelength, power - splitter_osa_loss

def filter_wavelength(wavelength, power, wl_0, wl_1):
    """Function to filter wavelength to a desired region.

    Inputs:
    - wavelength: array of wavelength values
    - power: array of power values
    - wl_0: lower bound of the wavelength region
    - wl_1: upper bound of the wavelength region

    Outputs:
    - wavelength: array of filteredwavelength values
    - power: array of filteredpower values"""

    wavelength_filtered = wavelength[(wavelength >= wl_0) & (wavelength < wl_1)]
    power_filtered = power[(wavelength >= wl_0) & (wavelength < wl_1)]
    
    return wavelength_filtered, power_filtered

def find_minima(power, wavelength, threshold, separation):
    '''Function to find minima in the power spectrum.

    Inputs:
    - power: array of power values
    - wavelength: array of wavelength values
    - threshold: minimum prominence of the peaks
    - separation: minimum distance between peaks

    Outputs:
    - indices: array of indices of the found minima
    '''

    power_inverted = -power

    # Calculate average step size in wavelength and convert separation from nm to number of points based on average step size
    avg_step = np.mean(np.diff(wavelength)) 
    dist_points = int(separation/avg_step) 

    indices, properties = find_peaks(power_inverted, prominence=threshold, distance=dist_points)

    return indices