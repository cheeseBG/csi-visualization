import pandas as pd
import numpy as np
import importlib
import config
decoder = importlib.import_module(f'decoders.{config.decoder}') # This is also an import

# Define file name
one_pcap_filename = 'one3.pcap'
zero_pcap_filename = 'zero1.pcap'

# Define file path
one_pcap_filepath = '/'.join(['../' + config.pcap_fileroot, one_pcap_filename])
zero_pcap_filepath = '/'.join(['../' + config.pcap_fileroot, zero_pcap_filename])

# Define number of features
feature_num = 100

# Define subcarrier index
'''
 null carrier index: 0, 1, 2, 3, 32 , 61, 62, 63
'''
sub = [7, 8, 14, 15, 20, 21, 40, 41, 54, 55]

# Data cutting
one_start_packet_num = 0  # defualt = 0
one_end_packet_num = 20000
zero_start_packet_num = 80000  # defualt = 0
zero_end_packet_num = 100000

file_name = sub.copy()

for i in range(0, len(sub)):
    if 4 <= sub[i] <= 31:
        sub[i] -= 4
    elif 33 <= sub[i] <= 60:
        sub[i] -= 5

subcarrier_idx = [idx for idx in sub]

if __name__ == "__main__":

    # Read pcap file and create dataframe
    try:
        one_samples = decoder.read_pcap(one_pcap_filepath)
    except FileNotFoundError:
        print(f'File {one_pcap_filepath} not found.')
        exit(-1)

    try:
        zero_samples = decoder.read_pcap(zero_pcap_filepath)
    except FileNotFoundError:
        print(f'File {zero_pcap_filepath} not found.')
        exit(-1)

    one_df = pd.DataFrame(np.abs(one_samples.get_all_csi(config.remove_null_subcarriers, config.remove_pilot_subcarriers)))
    zero_df = pd.DataFrame(np.abs(zero_samples.get_all_csi(config.remove_null_subcarriers, config.remove_pilot_subcarriers)))

    # Extract 60000 packets
    zero_df = zero_df[zero_start_packet_num:zero_end_packet_num]
    one_df = one_df[one_start_packet_num:one_end_packet_num]

    # All subcarrier dataframes will store here
    one_data_list = []
    zero_data_list = []

    '''
    Create label '1(one person)' data 
    '''
    for sub_idx in range(0, len(one_df.columns)):
        packet_num = 0
        subcarrier_array = []

        while (packet_num <= len(one_df) - feature_num):
            if packet_num == 0:
                subcarrier = one_df[sub_idx].iloc[packet_num:packet_num + feature_num]
                sub_array = np.array(subcarrier)
                subcarrier_array = sub_array.reshape(1, -1)
            else:
                subcarrier = one_df[sub_idx].iloc[packet_num:packet_num + feature_num]
                sub_array = np.array(subcarrier)
                sub_array = sub_array.reshape(1, -1)

                subcarrier_array = np.concatenate((subcarrier_array, sub_array), axis=0)

            packet_num += 100

        new_df = pd.DataFrame(subcarrier_array)

        # Add label '1(one person)' column in dataframe
        one_label = [1 for i in range(0, len(new_df))]
        new_df['label'] = one_label
        one_data_list.append(new_df)

    '''
    Create label '0(0 person)' data 
    '''
    for sub_idx in range(0, len(zero_df.columns)):
        packet_num = 0
        subcarrier_array = []

        while (packet_num <= len(zero_df) - feature_num):
            if packet_num == 0:
                subcarrier = zero_df[sub_idx].iloc[packet_num:packet_num + feature_num]
                sub_array = np.array(subcarrier)
                subcarrier_array = sub_array.reshape(1, -1)
            else:
                subcarrier = zero_df[sub_idx].iloc[packet_num:packet_num + feature_num]
                sub_array = np.array(subcarrier)
                sub_array = sub_array.reshape(1, -1)

                subcarrier_array = np.concatenate((subcarrier_array, sub_array), axis=0)

            packet_num += 100

        new_df = pd.DataFrame(subcarrier_array)

        # Add label '0(zero person)' column in dataframe
        zero_label = [0 for i in range(0, len(new_df))]
        new_df['label'] = zero_label
        zero_data_list.append(new_df)


    for idx in subcarrier_idx:
        print('# ' + str(idx) + ' subcarrier data(Label: 1)')
        print(one_data_list[idx])

    for idx in subcarrier_idx:
        print('# ' + str(idx) + ' subcarrier data(Label: 0)')
        print(zero_data_list[idx])


    # Concatenate two dataframe
    concat_list = []
    concat_df = pd.DataFrame()
    for idx in subcarrier_idx:
        concat_list.append(pd.concat([one_data_list[idx], zero_data_list[idx]]))

    for i in range(0, len(concat_list)):
        concat_df = pd.concat([concat_df, concat_list[i]])

    # Shuffle rows of dataframe and reindexing
    concat_df = concat_df.sample(frac=1).reset_index(drop=True)
    print(concat_df)

    # Save dataframe to excel file
    try:
       concat_df.to_excel('sub' + str(file_name) + '.xlsx')
    except:
        print('Fail to save data')







