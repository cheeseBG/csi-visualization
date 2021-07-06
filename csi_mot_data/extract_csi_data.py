from scapy.all import *
import config
import pandas as pd
import numpy as np
import time
decoder = importlib.import_module(f'decoders.{config.decoder}') # This is also an import


def func(pkt):
    global limit, count, timestamps
    timestamps.append(pkt.time)
    count = count + 1

    if count >= limit > 0:
        return True
    else:
        return False


if __name__ == "__main__":
    limit = 26000000
    count = 0
    timestamps = []
    filename = "../pcapfiles/class_0.pcap"

    # Read pcap file and create dataframe
    try:
        csi_samples = decoder.read_pcap(filename)
    except FileNotFoundError:
        print(f'File {filename} not found.')
        exit(-1)

    # Create CSI data frame
    csi_df = pd.DataFrame(np.abs(csi_samples.get_all_csi()))

    sniff(offline=filename, stop_filter=func, store=False)

    new_timestamp = []
    for arr_time in timestamps:
        num = len(str(arr_time % 1)) - 2
        new_timestamp.append(time.strftime("%a, %d %b %Y %H:%M:", time.localtime(arr_time)) + time.strftime("%S", time.localtime(arr_time))\
        + '.' + str(int(arr_time % 1 * (10 ** num))))

    csi_df.insert(0, 'time_stamp', new_timestamp)

    print(csi_df)

    # Save dataframe to excel file
    try:
        csi_df.to_csv('outputs.csv')
    except:
        print('Fail to save data')
