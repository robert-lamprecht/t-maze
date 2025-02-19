import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import re
import statistics
import shutil
import json 

folder_path = r'D:\TMAZE_DATA'
output_folder_path = r'C:\Users\pliu79\Downloads\Merged_TMAZE_DATA'

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

file_pattern = '*.json' 
files = glob.glob(os.path.join(folder_path, file_pattern)) 

file_groups = {}

for file in files:
    parts = os.path.basename(file).split('_')
    mouse_id = parts[1]
    date_str = parts[2]
    file_groups.setdefault((date_str, mouse_id), []).append(file)

# Merge files within each group
for group_key, group_filenames in file_groups.items():
    date_str, mouse_id = group_key
    output_filename = os.path.join(output_folder_path, f"merged_{mouse_id}_{date_str}.json")
    with open(output_filename, 'wb') as outfile:
        for filename in group_filenames:
            with open(filename, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)
                
for file in os.listdir(output_folder_path):
    if file.endswith('.json.json'):
        os.remove(os.path.join(output_folder_path, file))

print("Merged files saved in:", output_folder_path)