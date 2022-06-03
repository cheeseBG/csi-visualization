import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

from plot.dataPreprocess import data_preprocess
from datetime import datetime
'''
Heatmap
---------------------------

Plot 
'''


def heatmap(csi_df, sample_start, sample_end, isComp, preprocess=False):

    df = csi_df[sample_start:sample_end]

    if isComp == 'y':
        df = complexToAmp(df)

    if preprocess is True:
        df = data_preprocess(df)

    packet_idx = [i for i in range(1, len(df) + 1)]

    x_list = []
    for idx in packet_idx:
        x_list.append(idx)

    y_list = []
    for col in df.columns:
        y_list.append(col)

    plt.pcolor(x_list, y_list, df.transpose(), cmap='jet')
    cbar = plt.colorbar()
    cbar.set_label('Amplitude (dBm)')

    xtic = np.arange(0, x_list[-1] + 1, 100)
    xtic[0] = 1
    ytic = np.arange(0, 52, 13)

    plt.xticks(xtic)
    plt.yticks(ytic, [y_list[idx] for idx in [0, int(len(y_list)/4), int(len(y_list)/4*2), int(len(y_list)/4*3)]])
    plt.xlabel('Packet Index')
    plt.ylabel('Subcarrier Index')

    plt.show()


def timeHeatmap(csi_df, time_list, time_ms_list, isComp, preprocess=False):
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

    csi_df = csi_df[idx_list[0]:idx_list[-1] + 1]

    xtic_list = []

    for i in range(0, len(csi_df)):
        if i in new_idx_list:
            dtime = datetime.fromtimestamp(time_list[i + idx_list[0]])
            xtic_list.append(dtime.strftime("%H:%M:%S"))

    print('matching list {}'.format(xtic_list))

    if preprocess is True:
        csi_df = data_preprocess(csi_df)

    packet_idx = [i for i in range(1, len(csi_df) + 1)]

    x_list = []
    for idx in packet_idx:
        # x_list.append(idx / 150)
        x_list.append(idx)

    y_list = []
    for col in csi_df.columns:
        y_list.append(col)

    plt.pcolor(x_list, y_list, csi_df.transpose(), cmap='jet')
    cbar = plt.colorbar()
    cbar.set_label('Amplitude (dBm)')

    ytic = np.arange(0, 52, 13)

    plt.xticks(new_idx_list, xtic_list, rotation=45)
    plt.yticks(ytic, [y_list[idx] for idx in [0, int(len(y_list)/4), int(len(y_list)/4*2), int(len(y_list)/4*3)]])
    #plt.xlabel('Time (s)')
    plt.xlabel('Time')
    plt.ylabel('Subcarrier Index')

    plt.show()


def complexToAmp(comp_df):

    comp_df = comp_df.astype('complex')
    amp_df = comp_df.apply(np.abs, axis=1)

    return amp_df