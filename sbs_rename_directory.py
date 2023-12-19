import os

# Set the source directory
source_dir = "./viz_output/"

# Set the target prefix (e.g., "color")
target_prefix = "depth"

# Function to extract the frame number from the file name
def get_frame_number(filename):
    return int(filename.split("frame")[1].split(".")[0])

# List all files in the source directory
file_list = os.listdir(source_dir)

# Filter for only the frame*.png files and sort by frame number
frame_files = sorted([f for f in file_list if f.startswith("frame") and f.endswith(".png")], key=get_frame_number)

# Initialize a counter
counter = 0

# Iterate through the sorted files and rename them
for filename in frame_files:
    # Build the new file name
    new_name = f"{target_prefix}{counter}.png"

    # Rename the file
    os.rename(os.path.join(source_dir, filename), os.path.join(source_dir, new_name))

    # Increment the counter
    counter += 1

