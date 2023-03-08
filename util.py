import argparse
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def data_preprocess(csi_df):

    # Min-Max Normalization
    scaler = MinMaxScaler()
    scaler.fit(csi_df)
    scaled_df = scaler.transform(csi_df)
    csi_df = scaled_df

    return csi_df


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'True', 'TRUE', 'T', 'Y', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'False', 'FALSE', 'F', 'N', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def complexToAmp(comp_df):

    comp_df = comp_df.astype('complex')
    amp_df = comp_df.apply(np.abs, axis=1)

    return amp_df
