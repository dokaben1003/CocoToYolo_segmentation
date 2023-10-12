# CocoToYolo_segmentation

### Description

This utility script facilitates the easy and efficient conversion from COCO Annotation Format to YOLO Annotation Format.

### Features

- Conversion from COCO format JSON annotation files to YOLO format text annotation files.
- Loading of class indices and names mapping from a file.
- Proceeds with ignoring unknown/unrecognized classes.

### Requirements

- Python 3.x


### Usage

The script is run from the command line with arguments.

```shell
python coco_to_yolo.py --class_file /path/to/class.txt --coco_json /path/to/annotations.json --output_directory /path/to/output
```

### Arguments
```
--class_file : Path to the file with class names listed on each line.
--coco_json : Path to the JSON file containing COCO format annotations.
--output_directory : Path to the directory where YOLO format annotations should be saved.
```

### Output
The script will generate YOLO format annotation files in the specified output directory. Each text file will bear the name of the corresponding image file and contain YOLO-compatible annotations. 

### Note
The class.txt file must contain one class name per line. The output directory will be created by the script if it does not exist. Invalid paths will cause errors, so please ensure to provide the correct file paths.
