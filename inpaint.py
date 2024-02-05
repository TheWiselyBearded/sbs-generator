import os
import cv2
import numpy as np
import concurrent.futures
from threading import Lock
from skimage.restoration import inpaint_biharmonic
from skimage import img_as_float
from tqdm import tqdm

def create_mask_for_black_streaks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 2)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask

def inpaint_with_scikit(image, mask):
    # Convert image to float range [0, 1]
    image_float = img_as_float(image)  # Converts to float and scales [0, 1]

    # Ensure the mask is a boolean array
    mask_bool = mask.astype(bool)
    print(f"Image shape: {image_float.shape}")
    print(f"Mask shape: {mask.shape}")
    # Perform inpainting
    inpainted_image = inpaint_biharmonic(image_float, mask_bool, channel_axis=2)
    print("passed")
    # Convert the inpainted image back to uint8 if necessary
    inpainted_image_uint8 = (inpainted_image * 255).astype(np.uint8)

    return inpainted_image_uint8

def inpaint_black_streaks(image, mask):
    try:
        # Confirm or adjust image data type
        if image.dtype != np.uint8:
            print("Adjusting image data type to uint8")
            image = np.clip(image, 0, 255).astype(np.uint8)

        # Ensure mask is binary and of type np.uint8
        if mask.dtype != np.uint8 or np.unique(mask).tolist() not in [[0], [0, 255], [255]]:
            print("Adjusting mask data type to uint8 and ensuring it is binary")
            mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]

        print("About to start inpainting with cv2.inpaint")
        inpainted_image = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
        print("Inpainting completed successfully")

        return inpainted_image
    except Exception as e:
        print(f"Exception during inpainting: {e}")
        return image

def process_image_pair(paths, output_dir, frame_number, save_masks, lock):
    left_eye_image_path, right_eye_image_path = paths
    try:
        left_eye_image = cv2.imread(left_eye_image_path)
        right_eye_image = cv2.imread(right_eye_image_path)
        if left_eye_image is None or right_eye_image is None:
            print(f"Error: Image not found for frame {frame_number}")
            return
        
        if save_masks:
            with lock:  # Locking the inpainting operation
                left_eye_mask = create_mask_for_black_streaks(left_eye_image)
                right_eye_mask = create_mask_for_black_streaks(right_eye_image)                
                # left_eye_post = inpaint_black_streaks(left_eye_image, left_eye_mask)
                # right_eye_post = inpaint_black_streaks(right_eye_image, right_eye_mask)
                left_eye_post = inpaint_with_scikit(left_eye_image, left_eye_mask)
                right_eye_post = inpaint_with_scikit(right_eye_image, right_eye_mask)
                
            cv2.imwrite(os.path.join(output_dir, "leftEye", f"leftEyePost{frame_number}.jpg"), left_eye_post)
            cv2.imwrite(os.path.join(output_dir, "rightEye", f"rightEyePost{frame_number}.jpg"), right_eye_post)
        print(f"Completed frame {frame_number}")
    except Exception as e:
        print(f"Exception processing frame {frame_number}: {e}")

def main_process(input_dir, output_dir, save_masks=False):
    os.makedirs(output_dir, exist_ok=True)
    dirs_to_create = ["leftEye", "rightEye"]
    if save_masks:
        dirs_to_create += ["leftEyeMask", "rightEyeMask"]
    for dir_name in dirs_to_create:
        os.makedirs(os.path.join(output_dir, dir_name), exist_ok=True)
    
    left_path = os.path.join(input_dir, "leftEye")
    right_path = os.path.join(input_dir, "rightEye")
    left_eye_images = sorted([os.path.join(left_path, f) for f in os.listdir(left_path) if f.startswith('leftEye')])
    right_eye_images = sorted([os.path.join(right_path, f) for f in os.listdir(right_path) if f.startswith('rightEye')])
    
    lock = Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
        futures = [executor.submit(process_image_pair, paths, output_dir, idx+1, save_masks, lock)
                   for idx, paths in enumerate(zip(left_eye_images, right_eye_images))]
        list(tqdm(concurrent.futures.as_completed(futures), total=len(futures)))
    print("All image processing completed.")

if __name__ == "__main__":
    input_directory = "C:/Users/abahrema/Documents/Tools/sbs-generator/datasets/d0/scratch_test"
    output_directory = "C:/Users/abahrema/Documents/Tools/sbs-generator/datasets/d0/scratch_test_post"
    try:
        main_process(input_directory, output_directory, save_masks=True)
    except KeyboardInterrupt:
        print("Script execution was interrupted by the user. Exiting...")
        # Perform any cleanup here if necessary
        exit(0)