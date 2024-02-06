import os
import csv
import yaml
from PIL import Image

# open the yaml file
with open("signs-config.yaml", "r") as file:
    config = yaml.safe_load(file)
    names = config["names"]

def getIndexFromName(class_name : str):
    return list(names.keys())[list(names.values()).index(class_name)]


def convertToYoloAnnotation(file_name : str, class_name : str, x_uleft : int, y_uleft : int, x_lright : int, y_lright : int):
    # TODO: Fix x_center and y_center values, it is currently giving negative values for some reason
    
    # Returns: [class_id, x_center, y_center, normalized_width, normalized_height] (every val is between 0 & 1)
    
    # getting pixel size of the image
    img = Image.open(file_name)
    img_width, img_height = img.size

    # finding normalized width
    width = x_uleft - x_lright
    normalized_width = width / img_width

    # finding normalized height
    height = y_uleft - y_lright
    normalized_height = height / img_height
     
    # finding x center:
    x_center_pxl = (x_uleft + x_lright) / 2
    x_center = x_center_pxl / img_width

    # finding y center
    y_center_pxl = (y_uleft + y_lright) / 2
    y_center = y_center_pxl / img_height

    # getting class id

    class_id = getIndexFromName(class_name)
    
    return class_id, x_center, y_center, normalized_width, normalized_height




# TESTING
test = ["datasets/signs/aiua120214-0/frameAnnotations-DataLog02142012_external_camera.avi_annotations/speedLimit_1330545914.avi_image0.png",
         "speedLimit25", 	529,	183,	546, 203]

test_out = convertToYoloAnnotation(test[0], test[1], test[2], test[3], test[4], test[5])
print(test_out)