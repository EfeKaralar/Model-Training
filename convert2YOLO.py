import os
import csv
import yaml
from PIL import Image
import pandas as pd

UPPER_LIMIT = 300

annotation_source_path = "datasets/signs/allAnnotations.csv"
image_path = "datasets/signs/images/train"
label_path = "datasets/signs/labels/train"

# open the yaml file
with open("signs-config.yaml", "r") as file:
    config = yaml.safe_load(file)
    names = config["names"]

def getIndexFromName(class_name : str):
    return list(names.keys())[list(names.values()).index(class_name)]


def convertToYoloAnnotation(row):
    
    # Returns: [class_id, x_center, y_center, normalized_width, normalized_height] (every val is between 0 & 1)
    
    file_name, class_name = row['Filename'], row['Annotation tag']
    x_uleft, y_uleft = row['Upper left corner X'], row['Upper left corner Y']
    x_lright, y_lright = row['Lower right corner X'], row['Lower right corner Y']

    # getting pixel size of the image
    image_file_path = os.path.join(image_path, file_name)


    img = Image.open(image_file_path)
    img_width, img_height = img.size

    # finding normalized width
    width = abs(x_uleft - x_lright)
    normalized_width = width / img_width

    # finding normalized height
    height = abs(y_uleft - y_lright)
    normalized_height = height / img_height
     
    # finding x center:
    x_center_pxl = (x_uleft + x_lright) / 2.0
    x_center = x_center_pxl / img_width

    # finding y center
    y_center_pxl = (y_uleft + y_lright) / 2.0
    y_center = y_center_pxl / img_height

    # getting class id

    class_id = getIndexFromName(class_name)
    
    str_lst = [str(class_id), str(x_center), str(y_center), str(normalized_width), str(normalized_height)]
    out = ' '.join(str_lst)

    return out

    

# Read the CSV file
df = pd.read_csv(annotation_source_path,  sep=";")

# Group the data by image ID
grouped = df.groupby('Filename')

os.makedirs(label_path, exist_ok=True)

file_count = 0

# Iterate over the groups and create a .txt file for each image
for image_id, group in grouped:
    # Check if the image file exists
    image_file_path = os.path.join(image_path, image_id)
    if not os.path.exists(image_file_path):
        continue

    # Generate YOLO annotations for each bbox
    yolo_annotations = group.apply(convertToYoloAnnotation, axis=1) 
    # Concatenate the annotations into a single string with newline characters separating them
    yolo_annotations_str = '\n'.join(yolo_annotations)   
    # Write the YOLO annotations to a .txt file
    os.makedirs(os.path.dirname(os.path.join(label_path, image_id)), exist_ok=True)
    with open(os.path.join(label_path, f'{image_id[:image_id.rfind(".png")]}.txt'), 'w') as f:
        for annotation in yolo_annotations:
            f.write(f"{annotation}\n")
            file_count += 1

print("Number of files created:", file_count)

