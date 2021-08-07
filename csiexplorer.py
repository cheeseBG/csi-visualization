import time
import importlib
import config
from plotters.AmpPhaPlotter import Plotter# Amplitude and Phase plotter
from plotters.timePlotter import TimePlotter
from plotters.heatmap import Heatmap
decoder = importlib.import_module(f'decoders.{config.decoder}') # This is also an import


def string_is_int(s):
    '''
    Check if a string is an integer
    '''
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    pcap_filename = input('Pcap file name: ')

    if '.pcap' not in pcap_filename:
        pcap_filename += '.pcap'
    pcap_filepath = '/'.join([config.pcap_fileroot, pcap_filename])

    try:
        samples = decoder.read_pcap(pcap_filepath)
    except FileNotFoundError:
        print(f'File {pcap_filepath} not found.')
        exit(-1)

    while True:
        plot_mode = input('1.CSI_explore, 2.Time Domain plot, 3.Heatmap, 4.Exit: ')
        if plot_mode == '1':
            if config.plot_samples:
                plotter = Plotter(samples.bandwidth)

            while True:
                command = input('> ')

                if 'help' in command:
                    print(config.help_str)

                elif 'exit' in command:
                    break

                elif ('-' in command) and \
                        string_is_int(command.split('-')[0]) and \
                        string_is_int(command.split('-')[1]):

                    start = int(command.split('-')[0])
                    end = int(command.split('-')[1])

                    for index in range(start, end + 1):
                        if config.print_samples:
                            samples.print(index)
                        if config.plot_samples:
                            csi = samples.get_csi(
                                index,
                                config.remove_null_subcarriers,
                                config.remove_pilot_subcarriers
                            )
                            plotter.update(csi)

                        time.sleep(config.plot_animation_delay_s)

                elif string_is_int(command):
                    index = int(command)

                    if config.print_samples:
                        samples.print(index)
                    if config.plot_samples:
                        csi = samples.get_csi(
                            index,
                            config.remove_null_subcarriers,
                            config.remove_pilot_subcarriers
                        )
                        plotter.update(csi)
                else:
                    print('Unknown command. Type help.')
        elif plot_mode == '2':
            sub = input('subcarrier index(-32 ~ 32):  ')
            timePlotter = TimePlotter(samples.bandwidth, samples.get_subcarrier(int(sub)))
            #sub_carrier = samples.get_subcarrier(int(sub))
            timePlotter.plot()
        elif plot_mode == '3':
            pre = input('Data Preprocessing (True or False):  ')

            hm = Heatmap(samples.bandwidth, samples.get_all_csi(
                config.remove_null_subcarriers,
                config.remove_pilot_subcarriers))

            if pre is True:
                hm.plot(preprocess=True)
            elif pre is False:
                hm.plot()
            else:
                print('Wrong input!')
        elif plot_mode == '4':
            break
        else:
            print('Unknown command.')


