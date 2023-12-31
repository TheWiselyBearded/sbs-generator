import cv2
import numpy as np
import os
import typer

app = typer.Typer()

@app.command()
def process_images(
    input_dir: str = typer.Argument(..., help="Path to the input directory containing color and depth images"),
    output_dir: str = typer.Argument(..., help="Path to the output directory for left and right eye images"),
    scale_factor: float = typer.Option(0.05, help="Scale factor to adjust the depth effect"),
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    color_images = sorted([f for f in os.listdir(input_dir) if f.startswith('color')])
    depth_images = sorted([f for f in os.listdir(input_dir) if f.startswith('depth')])

    for color_image_path, depth_image_path in zip(color_images, depth_images):
        color_image = cv2.imread(os.path.join(input_dir, color_image_path))
        depth_map = cv2.imread(os.path.join(input_dir, depth_image_path), cv2.IMREAD_GRAYSCALE)

        if color_image is None:
            typer.echo(f"Error: Color image not found at {os.path.join(input_dir, color_image_path)}")
            continue

        if depth_map is None:
            typer.echo(f"Error: Depth map not found at {os.path.join(input_dir, depth_image_path)}")
            continue

        # Function to shift pixels based on depth map
        def shift_pixels(image, depth_map, direction):
            shifted_image = np.zeros_like(image)
            for y in range(image.shape[0]):
                for x in range(image.shape[1]):
                    disparity = calculate_disparity(depth_map[y, x])
                    new_x = x + disparity * direction
                    if 0 <= new_x < image.shape[1]:
                        shifted_image[y, new_x] = image[y, x]
            return shifted_image

        # Calculate disparity (example function, adjust as needed)
        def calculate_disparity(depth_value):
            # Simple linear mapping, adjust the scale factor as needed
            return int(depth_value * scale_factor)

        # Create left and right eye images
        left_eye_image = shift_pixels(color_image, depth_map, 1)
        right_eye_image = shift_pixels(color_image, depth_map, -1)

        frame_number = color_image_path.split('color')[1].split('.')[0]

        if not os.path.exists(os.path.join(output_dir,'leftEye')):
            os.makedirs(os.path.join(output_dir,'leftEye'))      
        if not os.path.exists(os.path.join(output_dir,'rightEye')):
            os.makedirs(os.path.join(output_dir,'rightEye'))
        
        left_eye_output_path = os.path.join(output_dir, f'leftEye/leftEye{frame_number}.jpg')
        right_eye_output_path = os.path.join(output_dir, f'rightEye/rightEye{frame_number}.jpg')

        # Save the left and right eye images
        cv2.imwrite(left_eye_output_path, left_eye_image)
        cv2.imwrite(right_eye_output_path, right_eye_image)


        typer.echo(f"Processed frame {frame_number}.")

if __name__ == "__main__":
    app()

