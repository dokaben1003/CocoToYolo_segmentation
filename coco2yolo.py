import json
import os
import glob
import argparse

def load_classes(class_file):
    """
    Load class indices and names from a file.

    Parameters:
    class_file (str): Path to the file containing class names, one per line.

    Returns:
    dict: A dictionary where keys are class names and values are corresponding indices.
    """
    with open(class_file, 'r') as file:
        classes = file.read().strip().split("\n")
    return {name: idx for idx, name in enumerate(classes)}

def convert_coco_to_yolo(coco_json, output_directory, class_mapping):
    """
    Convert annotations from COCO format to YOLO format.

    Parameters:
    coco_json (str): Path to the COCO annotations file in JSON format.
    output_directory (str): Directory where the YOLO annotation files will be saved.
    class_mapping (dict): A dictionary mapping class names to indices.

    Returns:
    None
    """
    # Load COCO data
    with open(coco_json, 'r') as file:
        coco_data = json.load(file)

    # Map COCO category IDs to category names
    category_mapping = {category['id']: category['name'] for category in coco_data['categories']}

    # Group annotations by image ID
    image_id_to_annotations = {}
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        if image_id not in image_id_to_annotations:
            image_id_to_annotations[image_id] = []
        image_id_to_annotations[image_id].append(annotation)

    # Process annotations for each image
    for image in coco_data['images']:
        image_id = image['id']
        image_name = os.path.splitext(image['file_name'])[0]  # Remove the file extension
        annotations = image_id_to_annotations.get(image_id, [])
        
        # Get image width and height
        image_width = image['width']
        image_height = image['height']

        # Create YOLO format annotations
        normalized_annotations = []
        for annotation in annotations:
            # Get COCO category ID, map it to class name, and then map to YOLO class ID
            coco_category_id = annotation['category_id']
            class_name = category_mapping[coco_category_id]
            yolo_class_id = class_mapping.get(class_name, -1)  # -1 is default for not found

            if yolo_class_id == -1:
                continue  # Skip if the class is not in class.txt

            # Convert bounding box to YOLO format
            bbox = annotation['bbox']
            x_center = (bbox[0] + bbox[2] / 2) / image_width
            y_center = (bbox[1] + bbox[3] / 2) / image_height
            width = bbox[2] / image_width
            height = bbox[3] / image_height

            yolo_annotation = f"{yolo_class_id} {x_center} {y_center} {width} {height}"
            normalized_annotations.append(yolo_annotation)

        # Create one text file for each image
        output_path = os.path.join(output_directory, f"{image_name}.txt")
        with open(output_path, 'w') as file:
            file.write("\n".join(normalized_annotations))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO format annotations to YOLO format.")
    parser.add_argument('--class_file', type=str, required=True, help='Path to class.txt file.')
    parser.add_argument('--coco_json', type=str, required=True, help='Path to the COCO annotations file in JSON format.')
    parser.add_argument('--output_directory', type=str, required=True, help='Directory where YOLO annotations should be saved.')
    args = parser.parse_args()

    class_mapping = load_classes(args.class_file)  # Load mapping of class names to indices

    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    # Directly process the specified JSON file
    convert_coco_to_yolo(args.coco_json, args.output_directory, class_mapping)

    print(f"YOLO format annotations saved to {args.output_directory}")
