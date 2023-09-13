import glob
import pandas as pd
import math
import os

def get_file_name(file_path):
    file_path_components = file_path.split('/')
    file_name_and_extension = file_path_components[-1].rsplit('.', 1)[0]
    if '_' in file_name_and_extension:
        file_name_without_extension = file_name_and_extension.split('_', 1)[0]
    else:
        file_name_without_extension = file_name_and_extension
    return file_name_without_extension

# To find the borders of granules (or any objects) in the shape of a cube
def find_border(dir_path):
    for filepath in glob.glob(os.path.join(dir_path, f'*.csv')):
        img_name = get_file_name(filepath)
        df1 = pd.read_csv(filepath)

        vol_col = df1.iloc[:, 10] 
        maj_rad_col = df1.iloc[:, 12] 
        centre_z_col = df1.iloc[:, 6] #pix
        centre_x_col = df1.iloc[:, 4] #pix
        centre_y_col = df1.iloc[:, 5] #pix

        # Get minor radius (assume as side length of square / 2)
        side_len_x_min = []
        side_len_x_max = []
        side_len_y_min = []
        side_len_y_max = []
        z_range_min = []
        z_range_max = []

        for vol, maj_rad, centre_x, centre_y, centre_z in zip(vol_col, maj_rad_col, centre_x_col, centre_y_col, centre_z_col):
            if vol <= 0 or maj_rad <= 0:
                side_len_x_min.append(-10)
                side_len_x_max.append(-10)
                side_len_y_min.append(-10)
                side_len_y_max.append(-10)
                z_range_min.append(-10)
                z_range_max.append(-10)
            else:
                min_rad = math.sqrt((3 * vol) / (4 * math.pi * maj_rad))
                side_len = (min_rad * 13.5692) + 2 # convert to pixels

                side_len_x_min.append(centre_x - side_len)
                side_len_x_max.append(centre_x + side_len)
                side_len_y_min.append(centre_y - side_len)
                side_len_y_max.append(centre_y + side_len)

                z_range_min.append(math.floor(centre_z - maj_rad))
                z_range_max.append(math.ceil(centre_z + maj_rad))

        # Store values
        df1['y_range_min'] = side_len_x_min
        df1['y_range_max'] = side_len_x_max
        df1['x_range_min'] = side_len_y_min
        df1['x_range_max'] = side_len_y_max
        df1['z_range_min'] = z_range_min
        df1['z_range_max'] = z_range_max

        #TODO Change this line for location of your laptop
        df1.to_csv(f'/Users/aliceliu/Desktop/Granule_Border/{img_name}_input.csv', sep='\t', index=False)

