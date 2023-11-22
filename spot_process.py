import pandas as pd
import numpy as np
import os.path
import glob
import statistics
from granule_process import get_file_name

def get_median(dir_path_1, dir_path_2, keyword, channel_name):
    filename_1 = f'*_{channel_name}_{keyword}.loc4'
    intensity = []
    for filepath_1 in glob.glob(os.path.join(dir_path_1, filename_1)):
        df1 = pd.read_table(filepath_1, delimiter='\t')
        for index, row in df1.iterrows():
            intensity.append(row['integratedIntensity'])
    for filepath_1 in glob.glob(os.path.join(dir_path_2, filename_1)):
        df1 = pd.read_table(filepath_1, delimiter='\t')
        for index, row in df1.iterrows():
            intensity.append(row['integratedIntensity'])
    print (statistics.median(intensity))
    return statistics.median(intensity)

# Returns file containing information on information on #RNA in spots
def get_spot_info(dir_path, keyword, filename, is_granule, channel_name, median_intensity):
    filename_1 = f'*_{channel_name}_{keyword}.loc4'
    print(filename_1)

    for filepath_1 in glob.glob(os.path.join(dir_path, filename_1)):
        # File containing spots info
        df1 = pd.read_table(filepath_1, delimiter='\t')
        image_num = get_file_name(filepath_1)
        # Accounts for granules
        if is_granule != "":
            # Output from find_border.py
            filepath_2 = f'/Users/aliceliu/Desktop/Granule_Border/{image_num}_input.csv'
            df2 = pd.read_table(filepath_2, delimiter='\t')

        num_rna_counts_granule = {}
        num_rna_counts_pcell = {}
        granule_size = []

        sheet_name_1 = f'{channel_name}_{keyword}_{is_granule}'
        out_file = f"{dir_path}/Spots_Data_{filename}_{sheet_name_1}.xlsx"

        for index1, row1 in df1.iterrows():
            val_x = row1['x_in_pix']
            val_y = row1['y_in_pix']
            val_z = row1['z_in_pix']
            intensity = row1['integratedIntensity']
            num_rna = round(intensity / median_intensity)
            granule_temp = 0
            if num_rna in num_rna_counts_pcell:
                num_rna_counts_pcell[num_rna] += 1
            else:
                num_rna_counts_pcell[num_rna] = 1
            # Account for granuules
            if is_granule != "":
                for index2, row2 in df2.iterrows():
                    y_range_min = row2['y_range_min']
                    y_range_max = row2['y_range_max']
                    x_range_min = row2['x_range_min']
                    x_range_max = row2['x_range_max']
                    z_range_min = row2['z_range_min']
                    z_range_max = row2['z_range_max']

                    granule_vol = row2['Vol (unit)']

                    # Compare if the value falls within the range
                    if y_range_min <= val_y <= y_range_max and x_range_min <= val_x <= x_range_max and z_range_min <= val_z <= z_range_max:

                        granule_temp = granule_vol

                        if num_rna in num_rna_counts_granule:
                            num_rna_counts_granule[num_rna] += 1
                        else:
                            num_rna_counts_granule[num_rna] = 1
                        break
            granule_size.append(granule_temp)
        df1['Granule Size'] = granule_size
        df1.to_csv(f'{dir_path}/{image_num}_{channel_name}_{keyword}.loc4', sep='\t', index=False)

        if os.path.exists(out_file):
            out_cur = pd.read_excel(out_file)
        else:
            # If the file doesn't exist, create an empty DataFrame
            out_cur = pd.DataFrame({"NumRNA": range(1, 41),
                                                "Num_Spots_With_X_Num_RNA_In_Granule": [0] * 40,
                                                "Num_Spots_With_X_Num_RNA_In_Area": [0] * 40})
        if is_granule != "":
            out_data = {"NumRNA": range(1, 41),
                                f"Num_Spots_With_X_Num_RNA_In_Granule_{image_num}": [num_rna_counts_granule.get(i, 0) for i in range(1, 41)],
                                f"Num_Spots_With_X_Num_RNA_In_Area_{image_num}": [num_rna_counts_pcell.get(i, 0) for i in range(1, 41)]}
        else:
            out_data = {"NumRNA": range(1, 41),
                                f"Num_Spots_With_X_Num_RNA_In_Area_{image_num}": [num_rna_counts_pcell.get(i, 0) for i in range(1, 41)]}
        
        out_df = pd.DataFrame(out_data)
        out_comb = out_cur.merge(out_df, on="NumRNA", how="outer")
        out_comb.to_excel(out_file, index=False, sheet_name=sheet_name_1)
        print("done")
