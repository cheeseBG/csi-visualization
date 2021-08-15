from sklearn.preprocessing import MinMaxScaler


def data_preprocess(csi_df):

    # Min-Max Normalization
    scaler = MinMaxScaler()
    scaler.fit(csi_df)
    scaled_df = scaler.transform(csi_df)
    csi_df = scaled_df

    return csi_df