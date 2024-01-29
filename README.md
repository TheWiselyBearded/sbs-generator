
# Side-by-Side (SBS) 3D Video Generation Framework

## Introduction
This repository contains a framework for converting monocular videos into side-by-side (SBS) 3D videos. It utilizes a combination of image processing techniques and depth map predictions to generate separate views for each eye, creating a 3D effect when viewed with appropriate hardware.

## Visualization of the Process
![Process Flow](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNng4cWdqczgwd3Q5MHRhZjhkYWgyajF1ajQyd29icnJxNzY3a2RvNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HZPYcBVGnOGgtEcpdW/giphy-downsized-large.gif)

*This GIF showcases the step-by-step transformation of a color video into an SBS 3D video. It visualizes the stages starting from the original color frames, generating depth maps, shifting images for left/right eye views, applying masks, and finally presenting the inpainted left/right eye views.*

## Libraries Utilized
- OpenCV: For image processing and video manipulation.
- NumPy: For numerical operations and array manipulations.
- Typer: For creating command-line interfaces in Python scripts.
- Marigold/PatchFusion/MiDAS: For depth map generation.
- FFMPEG: For video processing, separating and merging frames, injecting 3D metadata.

## Roadmap
- [ ] Add audio support to the final SBS 3D video.
- [ ] Easier-to-use parameters for controlling scale factor/depth effect.
- [ ] Simplified integration of depth prediction models (Marigold, PatchFusion, MiDAS).
- [ ] Accelerated performance in computational loops (e.g., inpainting, generating left/right eye views).
- [ ] Single Shell/Bash Script for automating the entire pipeline.


## Using the Jupyter Notebook
The provided Jupyter Notebook guides you through the entire process of generating SBS 3D videos. It includes detailed code cells for each step of the pipeline, explanatory notes, and the ability to execute the process in an interactive environment. Its purpose is to facilitate an understanding of each stage and to offer a hands-on approach to SBS 3D video creation.

### How to Use
1. **Setup**: Ensure all dependencies are installed.
2. **Run Each Cell**: Sequentially execute the cells, which will guide you through the process from start to finish.
3. **Customization**: Modify parameters and paths as needed to suit your dataset and requirements.


## Scripts Description

### `sbs_rename_directory.py`
- **Purpose**: Renames files in a specified directory for consistent processing.
- **Usage**: `python sbs_rename_directory.py {rgbd_frames}`

### `sbs_generate_stereoviews.py`
- **Purpose**: Generates left and right eye views from color and depth images.
- **Usage**: `python sbs_generate_stereoviews.py {stereo_input_dir} {stereo_output_dir}`

### `sbs_inpaint_stereoviews.py`
- **Purpose**: Inpaints black streaks in left and right eye images.
- **Usage**: `python sbs_inpaint_stereoviews.py {stereo_output_dir} {stereo_postprocess_dir}`

## Contributing
(Instructions on how contributors can help improve the framework, including coding standards, pull request process, etc.)

## License
<!-- Released under the [MIT license](LICENSE). -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The MIT License (MIT)

Copyright © 2023 Alireza Bahremand

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
