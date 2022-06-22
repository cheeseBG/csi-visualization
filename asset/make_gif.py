# from plot.ampPlotter import AmpSubcarrierFlowPlotter
# import pandas as pd
# import numpy as np
#
# csi_df = pd.read_csv('./data/sample/csi_sample.csv')
#
# csi_df = csi_df.iloc[:, 2:]
#
# AmpSubcarrierFlowPlotter(csi_df, 'y')

from moviepy.editor import *

clip = VideoFileClip('ampSubFlow.mp4', audio=False)
clip.write_gif('ampSubFlow.gif', fps=14, fuzz=1)