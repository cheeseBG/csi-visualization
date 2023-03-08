import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np
import pywt
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


def AmpPlotter(csi_df, sample_start, sample_end, fname, spf_sub_list=None):

    csi_df = csi_df[sample_start:sample_end]

    if spf_sub_list is not None:
        sub_csi_list = []

        for sub in spf_sub_list:
            sub_csi_list.append([sub, csi_df[sub].to_list()])

        # ============ Denoising with DWT ==================

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle('Amp-PacketIdx plot', fontsize=20)
        for sub_csi in sub_csi_list:
            ax.plot(sub_csi[1], alpha=0.5, label='sub ' + sub_csi[0])
        # rec = lowpassfilter(signal, 0.2)
        # ax.plot(rec, 'k', label='DWT smoothing}', linewidth=2)
        ax.legend()
        # ax.set_title('Removing High Frequency Noise with DWT', fontsize=18)
        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Packet Index', fontsize=16)
        plt.show()
    else:
        subcarrier_list = []
        for col in csi_df.columns:
            subcarrier_list.append(csi_df[col].to_list())

        # ============ Denoising with DWT ==================

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle(fname, fontsize=20)

        for idx, sub in enumerate(subcarrier_list):
            ax.plot(sub, alpha=0.5, label=csi_df.columns[idx])

        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Packet Index', fontsize=16)
        plt.show()


def AmpSubcarrierFlowPlotter(csi_df, sample_start, sample_end):
    csi_df = csi_df[sample_start:sample_end]
    x = np.arange(0, len(csi_df.columns), 1)
    y_list = []

    for packet in np.array(csi_df):
        y_list.append(list(packet))

    plt.ion()

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('Amp-SubcarrierIdx plot', fontsize=20)
    line, = ax.plot(x, y_list[0], alpha=0.5)

    plt.ylabel('Signal Amplitude', fontsize=16)
    plt.xlabel('Subcarrier Index', fontsize=16)
    plt.ylim(0, 1500)

    for i in range(1, len(y_list)):
        update_y = y_list[i]

        line.set_xdata(x)
        line.set_ydata(update_y)

        fig.canvas.draw()
        fig.canvas.flush_events()

        time.sleep(0.01)


def AmpSubcarrierPlotter(csi_df, sample_start, sample_end):
    csi_df = csi_df[sample_start:sample_end]

    packet_list = []
    for packet in np.array(csi_df):
        packet_list.append(list(packet))

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('Amp-SubcarrierIdx plot', fontsize=20)

    for idx, sub in enumerate(packet_list):
        ax.plot(sub, alpha=0.5)

    ax.set_ylabel('Signal Amplitude', fontsize=16)
    ax.set_xlabel('Subcarrier Index', fontsize=16)
    plt.show()


def AmpTimePlotter(csi_df, time_list, time_ms_list, fname, spf_sub=None):

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
        sub_csi_list = []

        for sub in spf_sub:
            sub_csi_list.append([sub, csi_df[sub].to_list()])

        # ============ Denoising with DWT ==================

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle('Amp-Time plot', fontsize=20)
        for sub_csi in sub_csi_list:
            ax.plot(sub_csi[1], alpha=0.5, label='sub ' + sub_csi[0])
        # rec = lowpassfilter(signal, 0.2)
        # ax.plot(rec, 'k', label='DWT smoothing}', linewidth=2)
        ax.legend()
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
        fig.suptitle('Amp-Time plot', fontsize=20)

        for idx, sub in enumerate(subcarrier_list):
            ax.plot(sub, alpha=0.5, label=csi_df.columns[idx])

        ax.set_xticks(new_idx_list, xtic_list, rotation=45)

        ax.set_ylabel('Signal Amplitude', fontsize=16)
        ax.set_xlabel('Time', fontsize=16)
        plt.show()