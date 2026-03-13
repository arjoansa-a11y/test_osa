from utils import plot_trace, save_trace
from lab_devices import Yeni, Opm, YAMLDOCUMENT

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

    # Connect to the OPM
    try:
        opm = Opm(
            resource_address = 'USB0::0x1313::0x8078::P0030943::INSTR',
        )
    except Exception as e:
        raise ConnectionError(f"Could not connect to OPM:\n {e}")
    # Configure the YAML document
    doc = YAMLDOCUMENT()
    doc.datetime = formatted
    doc.operator = 'Joan Aroca'
    doc.setup = 'P2.S2'
    doc.project = project = "PHYSIS"
    doc.wafer = wafer = "17753-4"
    doc.reticle = reticle = "2"
    doc.die = die_name = "5"
    doc.dut = dut = "u3"
    doc.polarization = polarization = 'nana'
    doc.die_temperature = "na" #kOhm Tacc
    doc.coupling_type = 'SM-SM'
    doc.idsource = "ASE1" #'FiberLabs ASE-FL7015 1530-1610nm'
    doc.idosa = 'OSA20' # "EXFO OSA20"
    doc.operator_notes = """NA"""
    doc.opm_power = opm.measure_power() #dBm
    doc.splitter = "1x2-95/5" #95% to OSA, 5% to OPM

    # Saving data
    home = expanduser("~")
    folder_lab = os.path.expandvars("./data")
    folder_measurements = "/".join([folder_lab,project,wafer,reticle,die_name])
    file_name = f"{dut}"
    file_path = "/".join([folder_measurements,file_name])

    # Work with the OSA
    with osa: 
        osa_idn = osa.id
        opm_idn = opm.id
        # osa.wait_for()
        print("Instrument ID:", osa_idn)
        print("Instrument ID:", opm_idn)

        # OSA settings
        tracename = 1
        averages = 5
        osa.setup_sweep(
            center_wavelength = 1565e-9,
            span = 80e-9,
            sweep_mode = 'SINGLE',
            sensitivity = -70,
        )
        osa.run_sweep(tracename, averages=averages)
        trace = osa.get_trace(tracename)
        print(f"Power measured by OPM: {opm.measure_power()} dBm")
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
