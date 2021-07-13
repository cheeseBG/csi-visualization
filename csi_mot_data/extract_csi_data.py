import importlib

from scapy.all import *
import config
import pandas as pd
import numpy as np
import time
#from tracking_db import tracking_db
decoder = importlib.import_module(f'decoders.{config.decoder}') # This is also an import

#db = tracking_db()

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

    # Decimal to Float
    ts_decimaltofloat = list(map(float, timestamps))

    # # Change Linux UTC time to KST time
    # timestamps_new = []
    # for ts in ts_decimaltofloat:
    #     timestamps_new.append(datetime.fromtimestamp(ts))
    #
    # # Insert Timestamps
    # csi_df.insert(0, 'time', timestamps_new)
    # print(csi_df)

    # Insert Timestamps
    csi_df.insert(0, 'time', ts_decimaltofloat)

    # Save dataframe to excel file
    try:
        csi_df.to_csv('outputs.csv')
    except Exception as e:
        print('Fail to save data: ', e)


    # # Rename Subcarriers Column Name
    # columns = {}
    # for i in range(0, 64):
    #     columns[i] = '_' + str(i)
    #
    # csi_df.rename(columns=columns, inplace=True)
    #
    # # Save dataframe to SQL
    # try:
    #     db.insert_csi(csi_df)
    # except Exception as e:
    #     print('Fail to save data\n', e)
