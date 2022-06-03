import pandas as pd
import os
from plot.ampPlotter import AmpPlotter, AmpTimePlotter
from plot.heatmap import heatmap, timeHeatmap

'''
   <<  Null & Pilot subcarriers on 2.4MHz >>
    
    Null: [x+32 for x in [-32, -31, -30, -29, 31,  30,  29,  0]]
    Pilot: [x+32 for x in [-21, -7, 21,  7]]
    
    Available number of subcarriers: 64-12 = 52
'''
# For Test time section, set milestone
time_ms_list = [
    # ######### Test1 ###########

    # '2022-04-06 13:55:40',  # Start
    # '2022-04-06 13:55:47',  # Leave Left-Bottom
    # '2022-04-06 13:55:53',  # Arrive Right-Top
    # '2022-04-06 13:55:58',  # Leave Right-Top
    # '2022-04-06 13:56:01',  # Arrive Right-Bottom
    # '2022-04-06 13:56:07',  # End

    # ######### Test2 ###########

    # '2022-04-06 16:46:14',  # Start
    # '2022-04-06 16:46:32',  # Leave Left-Bottom
    # '2022-04-06 16:46:36',  # Arrive Right-Top
    # '2022-04-06 16:46:53',  # Leave Right-Top
    # '2022-04-06 16:46:55',  # Arrive Right-Bottom
    # '2022-04-06 16:47:22',  # End

    # ######### Test3_3rasp ###########
    
    # '2022-04-06 17:00:00',  # Start
    # '2022-04-06 17:01:00',  # Leave Left-Bottom
    # '2022-04-06 17:01:04',  # Arrive Middle-Top
    # '2022-04-06 17:02:01',  # Leave Middle-Top
    # '2022-04-06 17:02:04',  # Arrive Right-Bottom
    # '2022-04-06 17:03:07',  # End

    '2022-05-02 16:53:04',  # Start
    '2022-05-02 16:54:00',  # End
]

# Path
# test_name = '0502test'
# data_path = '../data'
# data_path = os.path.join(data_path, test_name, 'csi')

test_name = 'pe'
data_path = '../data'
data_path = os.path.join(data_path, test_name)

csi_list = os.listdir(data_path)

null_pilot_col_list = ['_' + str(x+32) for x in [-32, -31, -30, -29, -21, -7, 0, 7, 21, 29, 30, 31]]

s_start = 0
s_end = -1


if __name__ == "__main__":
    print('== Choose csv file == ')

    for idx, csi_fname in enumerate(csi_list):
        print('{}: {}'.format(idx+1, csi_fname))

    is_true = True

    while is_true:
        try:
            select_num = int(input("Select: "))
            if select_num > len(csi_list) or select_num <= 0:
                print("Error!")
                continue
            else:
                is_true = False
        except:
            print("Error!")
            continue

    isComp = None
    while isComp not in ['y', 'n']:
        isComp = input('CSI data type is complex?(y or n):  ')

    data_fname = csi_list[select_num-1]

    data_path = os.path.join(data_path, data_fname)

    # Read csi.csv
    df = pd.read_csv(data_path)

    # Remove MAC address, timestamp
    # csi_df = df.iloc[:, 2:]

    # Remove MAC address, timestamp, label
    csi_df = df.iloc[:, 2:-1]

    # Create timestamp list
    time_list = df['time'].tolist()

    # Remove null & pilot subcarriers
    if null_pilot_col_list[0] in list(csi_df.columns):
        csi_df.drop(null_pilot_col_list, axis=1, inplace=True)

    while True:
        plot_mode = input('1.Amplitude-SampleNum plot\n'
                          '2.Amplitude-Time plot\n'
                          '3.Heatmap\n'
                          '4.Time-Heatmap\n'
                          '5.Exit\n'
                          'Select: ')

        if plot_mode == '1':
            # select specific subcarrier
            spf_subc = input('Select specific subcarrier(True or False):  ')

            if spf_subc == 'True':
                spf_sub_idx = input('Select one subcarrier {}:  '.format(csi_df.columns))

                while spf_sub_idx not in csi_df.columns:
                    print("Wrong input!")
                    spf_sub_idx = input('Select one subcarrier {}:  '.format(csi_df.columns))

                AmpPlotter(csi_df, s_start, s_end, isComp, spf_sub_idx)
            elif spf_subc == 'False':
                AmpPlotter(csi_df, s_start, s_end, isComp)
            else:
                print("Wrong input!")
        elif plot_mode == '2':
            # select specific subcarrier
            spf_subc = input('Select specific subcarrier(True or False):  ')

            if spf_subc == 'True':
                spf_sub_idx = input('Select one subcarrier {}:  '.format(csi_df.columns))

                while spf_sub_idx not in csi_df.columns:
                    print("Wrong input!")
                    spf_sub_idx = input('Select one subcarrier {}:  '.format(csi_df.columns))

                AmpTimePlotter(csi_df, time_list, time_ms_list, isComp, spf_sub_idx)
            elif spf_subc == 'False':
                AmpTimePlotter(csi_df, time_list, time_ms_list, isComp)
            else:
                print("Wrong input!")
        elif plot_mode == '3':
            pre = input('Data Preprocessing (True or False):  ')

            if pre == 'True':
                heatmap(csi_df, s_start, s_end, isComp, preprocess=True)
            elif pre == 'False':
                heatmap(csi_df, s_start, s_end, isComp)
            else:
                print("Wrong input!")
        elif plot_mode == '4':
            pre = input('Data Preprocessing (True or False):  ')

            if pre == 'True':
                timeHeatmap(csi_df, time_list, time_ms_list, isComp, preprocess=True)
            elif pre == 'False':
                timeHeatmap(csi_df, time_list, time_ms_list, isComp)
            else:
                print("Wrong input!")

        elif plot_mode == '5':
            break
        else:
            print('Unknown command.')


