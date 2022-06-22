'''
    ======= Plot type =======
    1.Amplitude-Packet Index (Default)
    2.Amplitude-Time
    3.Amplitude-Packet Heatmap
    4.Amplitude-Time Heatmap
    5.Amplitude-Subcarrier Index Flow
'''
import os
import argparse
import pandas as pd
import util

from cfg import config
from plot.ampPlotter import AmpPlotter, AmpTimePlotter
from plot.heatmap import heatmap, timeHeatmap


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('directory', type=str, help='name of CSI data directory')
parser.add_argument('-p', '--plt', type=int, default=1, help='Select Plot type')
parser.add_argument('--sub', type=util.str2bool, default=False, help='Use specific subcarriers(Boolean)')

args = parser.parse_args()

csi_dir = args.directory
use_specific_sub = args.sub

try:
    data_path = os.path.join('./data', csi_dir)
    csi_list = os.listdir(data_path)
except FileNotFoundError as e:
    print(e)
    print('Exit program')
    exit()

# Check Plot type index
plot_type_idx = args.plt
if not 1 <= plot_type_idx <= 4:
    print('Wrong Plot type Index!')
    exit()

# Read from config file
plot_params_dict = config.PLOT_PARAMETER
null_pilot_dict = config.NULL_PILOT_SUBCARRIER
extractor_dict = config.EXTRACTOR_CONFIG

# Time list for time plotter
time_ms_list = plot_params_dict['time']

# Delete or Not Null & Pilot subcarrier
del_null = plot_params_dict['del_null_sub']
del_pilot = plot_params_dict['del_pilot_sub']

bandwidth = extractor_dict['bandwidth']
null_list = null_pilot_dict['null_' + bandwidth]
pilot_list = null_pilot_dict['pilot_' + bandwidth]

use_sampling = plot_params_dict['sampling']

if use_sampling is True:
    # Sampling index (default is 0 to 1000)
    sampling_idx_list = plot_params_dict['sampling_idx']

# If use specific subcarriers(Not all subcarriers)
if use_specific_sub is True:
    sub_list = plot_params_dict['specific_subcarriers']


if __name__ == "__main__":

    for csi_fname in csi_list:

        csi_path = os.path.join(data_path, csi_fname)

        # Read csi.csv
        df = pd.read_csv(csi_path)

        # Remove MAC address, timestamp
        csi_df = df.iloc[:, 2:]

        # Create timestamp list
        time_list = df['time'].tolist()

        # Remove null & pilot subcarriers
        if del_null is True:
            csi_df.drop(null_list, axis=1, inplace=True)
        elif del_pilot is True:
            csi_df.drop(pilot_list, axis=1, inplace=True)

        # #####  Plot  #####

        # 1.Amplitude-Packet Index (Default)
        if plot_type_idx == 1:

            # Set sampling index
            if use_sampling is True:
                sample_start = sampling_idx_list[0]
                sample_end = sampling_idx_list[1]
            else:
                sample_start = 0
                sample_end = len(csi_df)

            # If use only few subcarriers
            if use_specific_sub is True:
                AmpPlotter(csi_df, sample_start, sample_end, sub_list)
            # Use all subcarriers
            else:
                AmpPlotter(csi_df, sample_start, sample_end)

        # Todo
        # elif plot_mode == '2':
        #     # select specific subcarrier
        #     spf_subc = input('Select specific subcarrier(True or False):  ')
        #
        #     if spf_subc == 'True':
        #         spf_sub_idx = input('Select one subcarrier {}:  '.format(csi_df.columns))
        #
        #         while spf_sub_idx not in csi_df.columns:
        #             print("Wrong input!")
        #             spf_sub_idx = input('Select one subcarrier {}:  '.format(csi_df.columns))
        #
        #         AmpTimePlotter(csi_df, time_list, time_ms_list, isComp, spf_sub_idx)
        #     elif spf_subc == 'False':
        #         AmpTimePlotter(csi_df, time_list, time_ms_list, isComp)
        #     else:
        #         print("Wrong input!")
        # elif plot_mode == '3':
        #     pre = input('Data Preprocessing (True or False):  ')
        #
        #     if pre == 'True':
        #         heatmap(csi_df, s_start, s_end, isComp, preprocess=True)
        #     elif pre == 'False':
        #         heatmap(csi_df, s_start, s_end, isComp)
        #     else:
        #         print("Wrong input!")
        # elif plot_mode == '4':
        #     pre = input('Data Preprocessing (True or False):  ')
        #
        #     if pre == 'True':
        #         timeHeatmap(csi_df, time_list, time_ms_list, isComp, preprocess=True)
        #     elif pre == 'False':
        #         timeHeatmap(csi_df, time_list, time_ms_list, isComp)
        #     else:
        #         print("Wrong input!")


