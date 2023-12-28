
# Side-by-Side (SBS) 3D Video Generation Framework

## Introduction
This repository contains a framework for converting monocular videos into side-by-side (SBS) 3D videos. It utilizes a combination of image processing techniques and depth map predictions to generate separate views for each eye, creating a 3D effect when viewed with appropriate hardware.

## Visualization of the Process
![Process Flow](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNng4cWdqczgwd3Q5MHRhZjhkYWgyajF1ajQyd29icnJxNzY3a2RvNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HZPYcBVGnOGgtEcpdW/giphy-downsized-large.gif)

*This GIF showcases the step-by-step transformation of a color video into an SBS 3D video. It visualizes the stages starting from the original color frames, generating depth maps, shifting images for left/right eye views, applying masks, and finally presenting the inpainted left/right eye views.*

## Installation
(Instructions on how to install and setup the framework, including dependencies like OpenCV, Typer, and ffmpeg.)

## Usage
(General instructions on how to use the framework, including command-line examples.)

## Using the Jupyter Notebook
The provided Jupyter Notebook guides you through the entire process of generating SBS 3D videos. It includes detailed code cells for each step of the pipeline, explanatory notes, and the ability to execute the process in an interactive environment. Its purpose is to facilitate an understanding of each stage and to offer a hands-on approach to SBS 3D video creation.

### How to Use
1. **Setup**: Ensure all dependencies are installed.
2. **Run Each Cell**: Sequentially execute the cells, which will guide you through the process from start to finish.
3. **Customization**: Modify parameters and paths as needed to suit your dataset and requirements.


## Scripts Description

### `sbs_rename_directory.py`
- **Purpose**: Renames files in a specified directory for consistent processing.
- **Usage**: (Example command and explanation of arguments.)

### `sbs_generate_stereoviews.py`
- **Purpose**: Generates left and right eye views from color and depth images.
- **Usage**: (Example command and explanation of arguments.)

### `sbs_inpaint_stereoviews.py`
- **Purpose**: Inpaints black streaks in left and right eye images.
- **Usage**: (Example command and explanation of arguments.)
- **Improvement Suggestions**: Enhanced error handling, optimizing mask creation, and performance optimization.

### `sbs-ffmpeg-shell.sh`
- **Purpose**: Utilizes ffmpeg to generate left and right eye videos and combine them into an SBS format.
- **Usage**: (Example command and explanation of arguments.)

## Contributing
(Instructions on how contributors can help improve the framework, including coding standards, pull request process, etc.)

## License
(Information about the license under which this framework is released.)
