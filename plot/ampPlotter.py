import numpy as np
import matplotlib.pyplot as plt
import pywt
import time

from plot.dataPreprocess import data_preprocess
from datetime import datetime


'''
Time plotter
---------------------------

Plot 
'''


def lowpassfilter(signal, thresh=0.63, wavelet="db4"):
    thresh = thresh * np.nanmax(signal)
    coeff = pywt.wavedec(signal, wavelet, mode="per", level=8)
    coeff[1:] = (pywt.threshold(i, value=thresh, mode="soft") for i in coeff[1:])
    reconstructed_signal = pywt.waverec(coeff, wavelet, mode="per")
    return reconstructed_signal


def AmpPlotter(csi_df, sample_start, sample_end, isComp, spf_sub=None):

    csi_df = csi_df[sample_start:sample_end]

    if isComp == 'y':
        csi_df = complexToAmp(csi_df)

    if spf_sub is not None:
        subcarrier = csi_df[spf_sub].to_list()

        # ============ Denoising with DWT ==================
        signal = subcarrier

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle('Amp-SampleIndex plot')
        ax.plot(signal, color="b", alpha=0.5, label=spf_sub)
        rec = lowpassfilter(signal, 0.2)
        ax.plot(rec, 'k', label='DWT smoothing}', linewidth=2)
        ax.legend()
        ax.set_title('Removing High Frequency Noise with DWT', fontsize=18)
        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Sample Index', fontsize=16)
        plt.show()
    else:
        subcarrier_list = []
        for col in csi_df.columns:
            subcarrier_list.append(csi_df[col].to_list())

        # ============ Denoising with DWT ==================

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle('Amp-SampleIndex plot')

        for idx, sub in enumerate(subcarrier_list):
            ax.plot(sub, alpha=0.5, label=csi_df.columns[idx])

        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Sample Index', fontsize=16)
        plt.show()


def AmpTimePlotter(csi_df, time_list, time_ms_list, isComp, spf_sub=None):
    if isComp == 'y':
        csi_df = complexToAmp(csi_df)

    # Change time_ms_list to Unix Time
    ut_ms_list = []
    for t in time_ms_list:
        ut_ms_list.append(time.mktime(datetime.strptime(t, '%Y-%m-%d %H:%M:%S').timetuple()))
    print('milestone list {}'.format(time_ms_list))

    # Find time milestone index
    idx_list = []
    for ut_idx, ms in enumerate(ut_ms_list):
        find_idx = False
        selected_idx = -1
        for idx, t in enumerate(time_list):
            # find start idx
            if t - ms >= 0 and ut_idx == 0:
                idx_list.append(idx)
                find_idx = True
                break
            # find another idx
            elif t - ms <= 0 and ut_idx != 0:
                selected_idx = idx
            elif t - ms > 0 and ut_idx != 0:
                idx_list.append(selected_idx)
                find_idx = True
                break

        if find_idx is False:
            idx_list.append(-1)

    if idx_list[0] == -1 or idx_list[-1] == -1:
        print("Test time is unmatched with CSI data time!!")
        print(idx_list)
        exit()

    # Plot
    new_idx_list = []
    for i in idx_list:
        if i - idx_list[0] >= 0:
            new_idx_list.append(i - idx_list[0])

    csi_df = csi_df[idx_list[0]:idx_list[-1]+1]

    xtic_list = []

    for i in range(0, len(csi_df)):
        if i in new_idx_list:
            dtime = datetime.fromtimestamp(time_list[i + idx_list[0]])
            xtic_list.append(dtime.strftime("%H:%M:%S"))

    print('matching list {}'.format(xtic_list))

    if spf_sub is not None:
        subcarrier = csi_df[spf_sub].to_list()

        # ============ Denoising with DWT ==================
        signal = subcarrier

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle('Amp-Time plot')
        ax.plot(signal, color="b", alpha=0.5, label=spf_sub)
        rec = lowpassfilter(signal, 0.2)
        ax.plot(rec, 'k', label='DWT smoothing}', linewidth=2)
        ax.set_xticks(new_idx_list, xtic_list, rotation=45)
        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Time', fontsize=16)
        plt.show()
    else:
        subcarrier_list = []
        for col in csi_df.columns:
            subcarrier_list.append(csi_df[col].to_list())

        # ============ Denoising with DWT ==================

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle('Amp-Time plot')

        for idx, sub in enumerate(subcarrier_list):
            ax.plot(sub, alpha=0.5, label=csi_df.columns[idx])

        ax.set_xticks(new_idx_list, xtic_list, rotation=45)

        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Time', fontsize=16)
        plt.show()


def complexToAmp(comp_df):

    comp_df = comp_df.astype('complex')
    amp_df = comp_df.apply(np.abs, axis=1)

    return amp_df
