import cv2
import numpy as np
import os
import argparse

def create_masks(annotation_file, image_file, output_directory):
    """
    Create mask images from annotations and save them along with the original image.

    Parameters:
    annotation_file (str): Path to the annotation file.
    image_file (str): Path to the image file.
    output_directory (str): Directory where the output files will be saved.

    Returns:
    None
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Load the image
    image = cv2.imread(image_file)

    # Get image dimensions
    image_height, image_width, _ = image.shape

    # Read annotation file
    with open(annotation_file, 'r') as file:
        lines = file.readlines()

    # Save original image
    original_image_output_path = os.path.join(output_directory, "original_image.png")
    cv2.imwrite(original_image_output_path, image)

    # Process each annotation line
    for i, line in enumerate(lines):
        values = line.strip().split()

        # Get class index
        class_index = int(values[0])

        # Retrieve bounding box coordinates (denormalize them)
        coordinates = [float(x) for x in values[1:]]
        num_points = len(coordinates) // 2
        points = [(coordinates[j], coordinates[j + 1]) for j in range(0, len(coordinates), 2)]
        points = [(int(x * image_width), int(y * image_height)) for x, y in points]

        # Create mask image
        mask = np.zeros((image_height, image_width), dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(points)], color=(255, 255, 255))  # Fill in white

        # Save mask image to file
        mask_output_path = os.path.join(output_directory, f"mask_for_class_{class_index}.png")
        cv2.imwrite(mask_output_path, mask)

if __name__ == "__main__":
    """
    Main function to handle command line arguments and execute the mask creation function.

    Returns:
    None
    """
    parser = argparse.ArgumentParser(description="Create mask images from annotations.")
    parser.add_argument('--annotation_file', type=str, required=True, help='Path to the annotation file.')
    parser.add_argument('--image_file', type=str, required=True, help='Path to the image file.')
    parser.add_argument('--output_directory', type=str, required=True, help='Directory where the output files will be saved.')
    args = parser.parse_args()

    create_masks(args.annotation_file, args.image_file, args.output_directory)

