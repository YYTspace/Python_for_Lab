

from TPM.BinaryImage import BinaryImage
from TPM.DataToSave import DataToSave
from TPM.localization import select_folder
import time
import pandas as pd
import numpy as np
import os
from glob import glob

analyzed_mode = '50'  ## if analyzed_mode = 'all', analyze all frames of .csv file
frame_n = 50



def get_analyzed_sheet(path_folder, analyzed_mode, frame_n):
    path_data = glob(os.path.join(path_folder, '*-fitresults.csv'))[0]
    t1 = time.time()
    Glimpse_data = BinaryImage(path_folder)
    if analyzed_mode == 'all':
        frame_n = Glimpse_data.frames_acquired
    df = pd.read_csv(path_data)
    bead_number = int(max(1 + df['aoi']))
    tracking_results = np.array(df)
    tracking_results = tracking_results[0:bead_number*frame_n, :]
    localization_results = np.zeros((bead_number, 1))
    Save_df = DataToSave(tracking_results, localization_results, path_folder, avg_fps=Glimpse_data.avg_fps, window=20, factor_p2n=10000/180)
    Save_df.save_all_dict_df_to_excel(title='snapshot')
    time_spent = time.time() - t1
    print('spent ' + str(time_spent) + ' s')



if __name__ == "__main__":
    path_folder = select_folder()
    path_folders = glob(os.path.join(path_folder, '*'))
    for path_folder in path_folders:
        get_analyzed_sheet(path_folder, analyzed_mode, frame_n)
