import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
import time
from datetime import datetime

def AmpRTPlotter(csi_df, spf_sub=None):
    subcarrier_list = []
    for col in csi_df.columns:
        subcarrier_list.append(csi_df[col].to_list())


    x = np.arange(0, 100, 1)
    y_list = []


    for i in range(0, len(subcarrier_list)):
        y_list.append([0 for j in range(0, 100)])

    plt.ion()

    fig, ax = plt.subplots(figsize=(12, 8))

    line_list = []

    for y in y_list:
        line, = ax.plot(x, y, alpha=0.5)
        line_list.append(line)

    plt.ylabel('Signal Amplitude', fontsize=16)
    plt.xlabel('Packet', fontsize=16)
    plt.ylim(0, 1500)

    # Amp Min-Max gap text on plot figure
    txt = ax.text(40, 1600, 'Amp Min-Max Gap: None', fontsize=14)
    gap_count = 0

    minmax = []

    idx = 999
    for l in range(0, 1000):
        idx += 1
        for i, y in enumerate(y_list):
            del y[0]
            new_y = subcarrier_list[i][idx]
            y.append(new_y)
            line_list[i].set_xdata(x)
            line_list[i].set_ydata(y)

            # Min-Max Gap
            if gap_count == 0:
                minmax.append([new_y, new_y])
            else:
                # Update min
                if minmax[i][0] > new_y:
                    minmax[i][0] = new_y
                # Update max
                if minmax[i][1] < new_y:
                    minmax[i][1] = new_y

        gap_list = []
        for mm in minmax:
            gap_list.append(mm[1] - mm[0])

        gap = max(gap_list)

        Artist.remove(txt)
        txt = ax.text(40, 1600, 'Amp Min-Max Gap: {}'.format(gap), fontsize=14)
        gap_count += 1
        if gap_count == 20:
            gap_count = 0
            minmax = []

        fig.canvas.draw()
        fig.canvas.flush_events()

        time.sleep(0.01)


if __name__ == '__main__':
    # Path
    test_name = 'sample'
    data_path = '../data'
    data_path = os.path.join(data_path, test_name, 'csi_sample.csv')
    #csi_list = os.listdir(data_path)

    null_pilot_col_list = ['_' + str(x + 32) for x in [-32, -31, -30, -29, -21, -7, 0, 7, 21, 29, 30, 31]]

    # Read csi.csv
    df = pd.read_csv(data_path)

    # Remove MAC address, timestamp
    csi_df = df.iloc[:, 2:]

    # Create timestamp list
    time_list = df['time'].tolist()

    # Remove null & pilot subcarriers
    # csi_df.drop(null_pilot_col_list, axis=1, inplace=True)

    AmpRTPlotter(csi_df)



