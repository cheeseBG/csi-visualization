import numpy as np
import matplotlib.pyplot as plt
import config

'''
Time plotter
---------------------------

Plot 
'''

__all__ = [
    'TimePlotter'
]


class TimePlotter():
    def __init__(self, bandwidth, subcarrier):
        self.bandwidth = bandwidth
        self.subcarrier = subcarrier

        self.x_amp = np.arange(0, len(subcarrier))
        self.x_pha = np.arange(0, len(subcarrier))

        self.fig, axs = plt.subplots(2)

        self.ax_amp = axs[0]
        self.ax_pha = axs[1]

        self.fig.suptitle('Time-Subcarrier plot')

    def plot(self):
        # These are also cleared with clear()
        self.ax_amp.set_ylabel('Amplitude')
        self.ax_pha.set_ylabel('Phase')
        self.ax_pha.set_xlabel('Packet')

        try:
            self.ax_amp.plot(self.x_amp, np.abs(self.subcarrier))
            self.ax_pha.plot(self.x_pha, np.angle(self.subcarrier, deg=True))

        except ValueError as err:
            print(
                f'A ValueError occurred. Is the bandwidth {self.bandwidth} MHz correct?\nError: ', err
            )
            exit(-1)

        plt.show()

    def __del__(self):
        pass
