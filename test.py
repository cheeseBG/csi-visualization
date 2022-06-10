from plot.ampPlotter import AmpSubcarrierPlotter
import pandas as pd
import numpy as np

csi_df = pd.read_csv('./data/sample/csi_sample.csv')

csi_df = csi_df.iloc[:, 2:]

AmpSubcarrierPlotter(csi_df, 'y')
