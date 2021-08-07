import numpy as np
import matplotlib.pyplot as plt
import config
import pandas as pd
from preprocessing import data_preprocess

'''
Heatmap
---------------------------

Plot 
'''

__all__ = [
    'Heatmap'
]


class Heatmap():
    def __init__(self, bandwidth, csi):
        self.bandwidth = bandwidth
        self.csi = csi

        self.nsub = int(bandwidth * 3.2)

        # Remove null subcarrier - jji
        if config.remove_null_subcarriers and bandwidth == 20:
            self.nsub -= 8

    def plot(self, preprocess=False):

        df = pd.DataFrame(np.abs(self.csi))
        #df = df[:20000]

        if preprocess is True:
            df = data_preprocess(df)

        plt.pcolor(df)
        #plt.xticks(np.arange([-32, -16, 0, 16, 32]))
        #plt.yticks(np.arange(0, len(df.index), 1), df.index)
        plt.title('CSI heatmap')
        plt.xlabel('Subcarrier')
        plt.ylabel('Packets')
        plt.colorbar()
        plt.show()
        plt.show()

    def __del__(self):
        pass
