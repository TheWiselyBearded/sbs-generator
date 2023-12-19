import cv2
import numpy as np
import os
import typer

app = typer.Typer()

def create_mask_for_black_streaks(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use adaptive thresholding to better capture the black streaks
    mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 8) # og 11 2
    
    # Dilate the mask to include the edges of the black streaks
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    return mask

def inpaint_black_streaks(image, mask):
    # Inpaint the black streaks in the image
    inpainted_image = cv2.inpaint(image, mask, 5, cv2.INPAINT_TELEA)
    
    return inpainted_image

@app.command()
def process_images(
    input_dir: str = typer.Argument(..., help="Path to the input directory containing left and right eye image pairs"),
    output_dir: str = typer.Argument(..., help="Path to the output directory for processed images"),
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    left_eye_images = sorted([f for f in os.listdir(input_dir) if f.startswith('leftEye')])
    right_eye_images = sorted([f for f in os.listdir(input_dir) if f.startswith('rightEye')])

    for left_eye_image_path, right_eye_image_path in zip(left_eye_images, right_eye_images):
        left_eye_image = cv2.imread(os.path.join(input_dir, left_eye_image_path))
        right_eye_image = cv2.imread(os.path.join(input_dir, right_eye_image_path))

        if left_eye_image is None:
            typer.echo(f"Error: Left eye image not found at {os.path.join(input_dir, left_eye_image_path)}")
            continue

        if right_eye_image is None:
            typer.echo(f"Error: Right eye image not found at {os.path.join(input_dir, right_eye_image_path)}")
            continue

        # Create masks for the black streaks in both left and right eye images
        left_eye_mask = create_mask_for_black_streaks(left_eye_image)
        right_eye_mask = create_mask_for_black_streaks(right_eye_image)

        # Inpaint the black streaks in both left and right eye images
        left_eye_post = inpaint_black_streaks(left_eye_image, left_eye_mask)
        right_eye_post = inpaint_black_streaks(right_eye_image, right_eye_mask)

        frame_number = left_eye_image_path.split('leftEye')[1].split('.')[0]
        left_eye_post_output_path = os.path.join(output_dir, f'leftEyePost{frame_number}.jpg')
        right_eye_post_output_path = os.path.join(output_dir, f'rightEyePost{frame_number}.jpg')
        left_eye_mask_output_path = os.path.join(output_dir, f'leftEyeMask{frame_number}.jpg')
        right_eye_mask_output_path = os.path.join(output_dir, f'rightEyeMask{frame_number}.jpg')

        # Save the processed images and masks
        cv2.imwrite(left_eye_post_output_path, left_eye_post)
        cv2.imwrite(right_eye_post_output_path, right_eye_post)
        cv2.imwrite(left_eye_mask_output_path, left_eye_mask)
        cv2.imwrite(right_eye_mask_output_path, right_eye_mask)

        typer.echo(f"Processed frame {frame_number}.")

if __name__ == "__main__":
    app()

