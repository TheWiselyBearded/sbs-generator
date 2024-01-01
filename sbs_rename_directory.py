import os
import re
import typer

app = typer.Typer()

def get_frame_number(filename):
    match = re.search(r"frame(\d+)_", filename)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"Invalid filename format: {filename}")

@app.command()
def rename_files(source_dir: str = typer.Argument(..., help="Path to the input directory containing color and depth images")):
    os.makedirs(source_dir, exist_ok=True)

    # Process color images
    color_files = sorted([f for f in os.listdir(source_dir) if f.startswith("frame") and f.endswith(".jpg")], 
                         key=lambda x: int(x.split("frame")[1].split(".")[0]))
    counter = 0
    for filename in color_files:
        new_name = f"color{counter}.jpg"
        os.rename(os.path.join(source_dir, filename), os.path.join(source_dir, new_name))
        counter += 1
    print(f"Renamed {counter} color files in {source_dir}.")

    # Process depth images
    depth_files = sorted([f for f in os.listdir(source_dir) if f.startswith("frame") and f.endswith(".png")], 
                         key=get_frame_number)
    counter = 0
    for filename in depth_files:
        new_name = f"depth{counter}.png"
        os.rename(os.path.join(source_dir, filename), os.path.join(source_dir, new_name))
        counter += 1
    print(f"Renamed {counter} depth files in {source_dir}.")

if __name__ == "__main__":
    app()
