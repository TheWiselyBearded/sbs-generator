import os

dataset_directory = 'datasets/d3/'

source_dir =  dataset_directory + "rgbd_in/"
os.makedirs(source_dir, exist_ok=True)
target_prefix = "color"

def get_frame_number(filename):
    return int(filename.split("frame")[1].split(".")[0])


file_list = os.listdir(source_dir)
frame_files = sorted([f for f in file_list if f.startswith("frame") and f.endswith(".jpg")], key=get_frame_number)
counter = 0

for filename in frame_files:
    new_name = f"{target_prefix}{counter}.jpg"
    os.rename(os.path.join(source_dir, filename), os.path.join(source_dir, new_name))
    counter += 1

target_prefix = "depth"

def get_frame_number(filename):
    return int(filename.split("frame")[1].split(".")[0])


file_list = os.listdir(source_dir)
frame_files = sorted([f for f in file_list if f.startswith("frame") and f.endswith(".png")], key=get_frame_number)
counter = 0

for filename in frame_files:
    new_name = f"{target_prefix}{counter}.png"
    os.rename(os.path.join(source_dir, filename), os.path.join(source_dir, new_name))
    counter += 1