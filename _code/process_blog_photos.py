import os
import sys
import glob
import math
from PIL import Image

path_to_process = "./assets/img/blog/20250220/"

### 1) convert iphone jfif to jpg
#
# get all jfif images in folder
images = glob.glob(path_to_process + "*.jfif")
for image in images:
    img = Image.open(image)
    fname = img.filename.split("\\")[1]
    print(fname)
    new_fname = fname.replace(".jfif",".jpg")
    print(new_fname)
    img.save(path_to_process + new_fname)
# Delete jfifs
images = glob.glob(path_to_process + "*.jfif")
for image in images:
    os.remove(image)    

### 2) convert camera JPG to jpg
#

# get all jfif images in folder
images = glob.glob(path_to_process + "*.JPG")
for image in images:
    img = Image.open(image)
    fname = img.filename.split("\\")[1]
    print(fname)
    new_fname = fname.replace(".JPG",".jpg")
    img.save(path_to_process + new_fname)

### 3)  now create thumbnails for all jpgs
#

# get all jpg images in folder
images = glob.glob(path_to_process + "*.jpg")

for image in images:
    # default size of thumbnail
    base_width = 204
    # load image and get filename
    img = Image.open(image)
    fname = img.filename.split("\\")[1]
    print(fname)
    # determine 10% of original width
    tenpercent = 0.1*float(img.size[0])

    # select largest value: 204 or 0.1x orig width
    if tenpercent > base_width:
        base_width = math.floor(tenpercent)

    print(tenpercent, base_width)

    # do maths to determine new height according to scaled width change
    percent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(percent)))
    # rescale image and save as thumbnail
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img.save(path_to_process + "s/" + fname)
