import numpy as np
import matplotlib.pyplot as plt
import pywt
import config
from plotters.dataPreprocess import data_preprocess

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

        # Todo: preprocssing 적용


        self.x_amp = np.arange(0, len(subcarrier))
        self.x_pha = np.arange(0, len(subcarrier))

        self.fig, axs = plt.subplots(2)

        self.ax_amp = axs[0]
        self.ax_pha = axs[1]

        self.fig.suptitle('Time-Subcarrier plot')

    def plot(self):
        # # These are also cleared with clear()
        # self.ax_amp.set_ylabel('Amplitude')
        # self.ax_pha.set_ylabel('Phase')
        # self.ax_pha.set_xlabel('Packet')
        #
        # try:
        #     self.ax_amp.plot(self.x_amp, np.abs(self.subcarrier))
        #     self.ax_pha.plot(self.x_pha, np.angle(self.subcarrier, deg=True))
        #
        # except ValueError as err:
        #     print(
        #         f'A ValueError occurred. Is the bandwidth {self.bandwidth} MHz correct?\nError: ', err
        #     )
        #     exit(-1)
        #
        # plt.show()

        # ============ Denoising with DWT ==================
        signal = np.abs(self.subcarrier)

        def lowpassfilter(signal, thresh=0.63, wavelet="db4"):
            thresh = thresh * np.nanmax(signal)
            coeff = pywt.wavedec(signal, wavelet, mode="per", level=8)
            coeff[1:] = (pywt.threshold(i, value=thresh, mode="soft") for i in coeff[1:])
            reconstructed_signal = pywt.waverec(coeff, wavelet, mode="per")
            return reconstructed_signal

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(signal, color="b", alpha=0.5, label='original signal')
        rec = lowpassfilter(signal, 0.2)
        ax.plot(rec, 'k', label='DWT smoothing}', linewidth=2)
        ax.legend()
        ax.set_title('Removing High Frequency Noise with DWT', fontsize=18)
        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Sample No', fontsize=16)
        plt.show()


    def __del__(self):
        pass
