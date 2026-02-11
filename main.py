from utils import plot_trace
from lab_devices import Yeni

def main():
    print("Hello from test-osa!")

    # Connect to the OSA
    try:
        osa = Yeni(
            resource_address = 'TCPIP0::192.168.54.1::5025::SOCKET',
        )
    except Exception as e:
        raise ConnectionError(f"Could not connect to OSA:\n {e}")


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

        # Plot the trace
        plot_trace(trace)

if __name__ == "__main__":
    main()
