import pandas as pd
import numpy as np
import glob
import os
from granule_process import get_file_name

# Returns files containing information on 2 different RNA spots that colocalizes
def get_colocalized_spots(dir_path, channel_name_1, channel_name_2, filename, keyword):
    
    filename_1 = f'*_{channel_name_1}_{keyword}.loc4'

    for filepath_1 in glob.glob(os.path.join(dir_path, filename_1)):
        filepath_2 = filepath_1.replace(channel_name_1, channel_name_2)
        filename_1 = get_file_name(filepath_1)
        filename_2 = get_file_name(filepath_2)

        df1 = np.loadtxt(filepath_1, delimiter='\t', skiprows=1)
        df2 = np.loadtxt(filepath_2, delimiter='\t', skiprows=1) 

        x_coordinates_df1 = df1[:, 0]
        x_coordinates_df2 = df2[:, 0]
        y_coordinates_df1 = df1[:, 1]
        y_coordinates_df2 = df2[:, 1]
        z_coordinates_df1 = df1[:, 2]
        z_coordinates_df2 = df2[:, 2]

        count_colocalize = 0
        num_spots_C1 = len(df1)
        num_spots_C2 = len(df2)

        difference_x = np.abs(x_coordinates_df1[:, np.newaxis] - x_coordinates_df2)
        difference_y = np.abs(y_coordinates_df1[:, np.newaxis] - y_coordinates_df2)
        difference_z = np.abs(z_coordinates_df1[:, np.newaxis] - z_coordinates_df2)
        count_colocalize = np.sum((difference_x + difference_y < 2) & (difference_z < 2))

        # Find rows that colocalizes (difference in pixel distance under threshold)
        threshold = 2
        colocalize_mask = ((np.abs(difference_x) < threshold) &
                        (np.abs(difference_y) < threshold) &
                        (np.abs(difference_z) < threshold))

        is_colocalized_C1 = df1[colocalize_mask.any(axis=1)]
        is_colocalized_C2 = df2[colocalize_mask.any(axis=0)]

        colocalized_df_C1 = pd.DataFrame(is_colocalized_C1)
        colocalized_df_C1.rename(columns = {0: 'x_in_pix', 1: 'y_in_pix', 2: 'z_in_pix', 
                                            3: 'integratedIntensity', 4: 'residual', 5: 'Image_number', 6: 'Granule Size'}, inplace=True)
        colocalized_df_C1.to_csv(f'{dir_path}/{filename_1}_{channel_name_1}_{keyword}_colocalized.loc4', sep='\t', index=False)

        colocalized_df_C2 = pd.DataFrame(is_colocalized_C2)
        colocalized_df_C2.rename(columns = {0: 'x_in_pix', 1: 'y_in_pix', 2: 'z_in_pix', 
                                            3: 'integratedIntensity', 4: 'residual', 5:'Image_number', 6: 'Granule Size'}, inplace=True)
        colocalized_df_C2.to_csv(f'{dir_path}/{filename_2}_{channel_name_2}_{keyword}_colocalized.loc4', sep='\t', index=False)
        #This file gets overwritten
        out_file = f"/Users/aliceliu/Desktop/Spots_Coloc_Data_{filename}_{keyword}.xlsx"

        data = {
        'image_num': [filename_1],
        'count_colocalize': [count_colocalize],
        'num_spots_C1': [num_spots_C1],
        'num_spots_C2': [num_spots_C2],
        }

        out_df = pd.DataFrame(data)

        if os.path.exists(out_file):
            out_cur = pd.read_excel(out_file)
            out_comb = out_cur.merge(out_df, how="outer")
            out_comb.to_excel(out_file, index=False)
        else:
            out_df.to_excel(out_file, index=False)
