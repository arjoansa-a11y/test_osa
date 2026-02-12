from utils import plot_trace, save_trace
from lab_devices import Yeni, YAMLDOCUMENT

import os, datetime, time
from os.path import isfile, expanduser

timestamp = datetime.datetime.fromtimestamp(time.time())
formatted = timestamp.strftime("%Y_%m_%d_%H_%M_%S")
UNDEFINED = "UNDEFINED"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

def main():
    print("Hello from test-osa!")

    # Connect to the OSA
    try:
        osa = Yeni(
            resource_address = 'TCPIP0::192.168.54.1::5025::SOCKET',
        )
    except Exception as e:
        raise ConnectionError(f"Could not connect to OSA:\n {e}")

    # Configure the YAML document
    doc = YAMLDOCUMENT()
    doc.datetime = formatted
    doc.operator = 'Camilo Cano'
    doc.setup = 'P2.S1'
    doc.project = project = UNDEFINED
    doc.wafer = wafer = UNDEFINED
    doc.reticle = reticle = UNDEFINED
    doc.die = die_name = UNDEFINED
    doc.dut = dut = "wvg"
    doc.polarization = polarization = 'nana'
    doc.die_temperature = "na" #kOhm Tacc
    doc.coupling_type = 'SM-SM'
    doc.idsource = "ASE1"#'FiberLabs ASE-FL7015 1530-1610nm'
    doc.idosa = 'OSA20' # "EXFO OSA20"
    doc.operator_notes = """NA"""

    # Saving data
    home = expanduser("~")
    folder_lab = os.path.expandvars("%USERPROFILE%\\data")
    folder_measurements = "\\".join([folder_lab,project,wafer,reticle,die_name])
    file_name = f"{dut}-{polarization}"
    file_path = "\\".join([folder_measurements,file_name])
    
    # Work with the OSA
    with osa: 
        osa_idn = osa.id
        # osa.wait_for()
        print("Instrument ID:", osa_idn)

        # OSA settings
        tracename = 1
        averages = 5
        osa.setup_sweep(
            center_wavelength = 1550e-9,
            span = 100e-9,
            sweep_mode = 'SINGLE',
            sensitivity = -65,
        )
        osa.run_sweep(tracename, averages=averages)
        trace = osa.get_trace(tracename)
        doc.coupler_2X2_90_10_SN = "none"
 
        ## Editing the yaml document
        doc.osa_idn = osa_idn
        doc.osa_resolution = osa.resolution_bandwidth
        doc.osa_sensitivity = osa.sensitivity_level
        doc.osa_start_wavelength = osa.wavelength_center-osa.wavelength_span/2 # do not use osa.start_wavelength it gives lot of digits
        doc.osa_stop_wavelength =  osa.wavelength_center+osa.wavelength_span/2 # do not use osa.stop_wavelength it gives lot of digits
        doc.osa_sweep_mode = osa.sweep_mode
        doc.osa_integrated_power = osa.integrated_power
        doc.osa_dBm_nm = osa.dBm_nm
                # Saving txt from osa measurement
        save_trace(folder_measurements=folder_measurements,
                file_name=file_name,
                yaml=doc,osa=osa,data=trace)
    # Plot the trace
    plot_trace(trace)

if __name__ == "__main__":
    main()
