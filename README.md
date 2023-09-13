# AirLocalize_Data_Process
Script to process AirLocalize data.

# How to use #
- Run python3 main.py -h for help with arguments
- Naming needs to be consistent with the following format: ***_{channel_name}_{keyword}.loc4** where keyword can be somatic/pcell for example. Assumes input files are loc4 files which is the output file extension from AirLocalize
- Path 1 and Path 2 are provided to be used to calculate desired median intenstiy from 1 or more folders

# Output #
- excel file containing following information
    1. RNA Per Spot In Somatic, P-Cell, or Granules.
    2. Co-localization of spots between RNA in 2 granules
    3. Output file will be stored in directory: **Spots_Data_{filename}_{channel_name}_{key_word}_{is_granule}.xlsx**
        - Do not use very long names for keyword/channel_name/is_granule/filename for a complete file name
- Output from granule_process.py; stored in separated location; {image_num}_input.csv
- Output from co_localize.py to be inputted into spot_process.py
    eg. Img-4_C1_colocalized