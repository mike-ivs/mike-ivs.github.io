import sys
import glob
import math
from PIL import Image

path_to_process = "./assets/img/blog/20250215/"

images = glob.glob(path_to_process + "*.jpg")

for image in images:
    base_width = 204
    img = Image.open(image)
    fname = img.filename.split("\\")[1]
    print(fname)
    tenpercent = 0.1*float(img.size[0])

    if tenpercent > base_width:
        base_width = math.floor(tenpercent)

    print(tenpercent, base_width)

    percent = (base_width / float(img.size[0]))

    hsize = int((float(img.size[1]) * float(percent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img.save(path_to_process + "s/" + fname)
