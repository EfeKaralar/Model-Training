import os
import csv
import yaml
from PIL import Image

UPPER_LIMIT = 5

annotation_source_path = "/home/alp/AVTPerception/February/AVT-Perception/datasets/signs/allAnnotations.csv"
train_path = "/home/alp/AVTPerception/February/AVT-Perception/datasets/signs/labels/train"


# open the yaml file
with open("signs-config.yaml", "r") as file:
    config = yaml.safe_load(file)
    names = config["names"]
    path = "datasets/signs"
    images_train_path = path + "/" + config.get("train")
    val_train_path = path + "/" + config.get("val")


def getTrueLocationFromCSV(file_name_in_csv : str):
    return "/home/alp/AVTPerception/February/AVT-Perception/datasets/signs/images/train" + "/" + file_name_in_csv


def getIndexFromName(class_name : str):
    return list(names.keys())[list(names.values()).index(class_name)]


def convertToYoloAnnotation(file_name : str, class_name : str, x_uleft : int, y_uleft : int, x_lright : int, y_lright : int):
    # TODO: Fix x_center and y_center values, it is currently giving negative values for some reason
    
    # Returns: [class_id, x_center, y_center, normalized_width, normalized_height] (every val is between 0 & 1)
    
    # getting pixel size of the image
    img = Image.open(file_name)
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
    
    return class_id, x_center, y_center, normalized_width, normalized_height

def createAnnotations():
    #os.chdir("/home/alp/AVTPerception/February/AVT-Perception")
    counter = 0
    with open(annotation_source_path) as csvFile:
        reader = csv.DictReader(csvFile, delimiter = ";")
        for row in reader:
            YOLO_formatted = convertToYoloAnnotation( getTrueLocationFromCSV(row["Filename"]), row["Annotation tag"],
                                   int(row["Upper left corner X"]), int(row["Upper left corner Y"]), 
                                   int(row["Lower right corner X"]), int(row["Lower right corner Y"]))
            createYoloAnnotation(row["Filename"] + ".txt", YOLO_formatted)
            if counter >= UPPER_LIMIT:
                return
            counter += 1
    

def createYoloAnnotation( file_name: str ,YOLO_formatted: tuple):
    os.chdir(train_path)
    with open(file_name, "a") as new_file:
        line = " ".join(YOLO_formatted) + "\n"
        new_file.write(line)


# TESTING

# Testing for convertion logic

# with open("./datasets/signs/allAnnotations.csv") as csvFile:
#     reader = csv.DictReader(csvFile, delimiter = ";")os.chdir("/home/alp/AVTPerception/February/AVT-Perception/datasets/signs/labels/train")
#     limiter = 0
#     for file_test in reader:
#         out = convertToYoloAnnotation( getTrueLocationFromCSV(file_test["Filename"]), file_test["Annotation tag"],
#                                    int(file_test["Upper left corner X"]), int(file_test["Upper left corner Y"]), 
#                                    int(file_test["Lower right corner X"]), int(file_test["Lower right corner Y"]))
#         print(out[0], out[1], out[2], out[3], out[4])
#         limiter += 1
#         # test for 5 values
#         if limiter == 5:
#             break


createAnnotations()