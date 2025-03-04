import os
import sys
import glob
import math
from PIL import Image

path_to_process = "./assets/img/blog/20250224/"
post_to_process = "./_posts/2025-02-24-act.md"


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

# get all JPG images in folder
images = glob.glob(path_to_process + "*.JPG")
for image in images:
    img = Image.open(image)
    fname = img.filename.split("\\")[1]
    new_fname = fname.replace(".JPG","_new.jpg")
    if fname != new_fname:
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


### 4) read in blog post and insert image code
#

# read file first, store contents, make additions, and rewrite the file
# in second step
new_data = []
# open post for reading
with open(post_to_process,"r") as f:
    lines = f.readlines()
    for line in lines:
        # find lines beginning with "* IMG " or "* VID "
        if line[:6] == "* IMG ":
            # strip out asterix and new line character
            line_photos = line.replace("* IMG ","").replace("\n","")
            line_photos = line_photos.split(",")

            # for single photo ignore extra div container and group comment
            if len(line_photos) == 1:
                new_data.append('<a class="spotlight" href="'+path_to_process[1:]+line_photos[0]+'.jpg">\n')
                new_data.append('    <img src="'+path_to_process[1:]+'s/'+line_photos[0]+'.jpg"/>\n')
                new_data.append('</a>\n')
            else:
                # rolling idx from 0 to 2 (temporarily 3 until zeroed)
                idx = 0
                # index to keep track of 3x groups
                group_id = 1
                # lenth of images to group, minus 1 if mod%=1
                len_to_group = len(line_photos)
                extra_single = False
                # detect if mod = 1 and flag + edit length
                if (len(line_photos) % 3) == 1:
                    len_to_group -= 1
                    extra_single = True

                # iterate over images to bundle together in code
                for p in line_photos[:len_to_group]:
                    # if 1st image out of 3 write div container wrapper
                    if not idx:
                        new_data.append('<!-- Group '+str(group_id)+' -->\n')
                        new_data.append('<div class="spotlight-group">\n')
                    # write image code
                    new_data.append('    <a class="spotlight" href="'+path_to_process[1:]+str(p)+'.jpg">\n')
                    new_data.append('        <img src="'+path_to_process[1:]+'s/'+str(p)+'.jpg"/>\n')
                    new_data.append('    </xxa>\n')
                    # increment counter
                    idx += 1
                    # if 3rd image processed, add end div container and change flags
                    if idx == 3:
                        new_data.append('</div>\n')
                        idx = 0
                        group_id +=1
                # if end of images and not a multiple of 3, add closing div (3 is closed already)
                if idx:
                    new_data.append('</div>\n')

                # if we had a mod%=1, add that extra image in by itself
                if extra_single:
                    new_data.append('<a class="spotlight" href="'+path_to_process[1:]+line_photos[-1]+'.jpg">\n')
                    new_data.append('    <img src="'+path_to_process[1:]+'s/'+line_photos[-1]+'.jpg"/>\n')
                    new_data.append('</a>\n')

        elif line[:6] == "* VID ":
            # strip out asterix and new line character
            line_vid = line.replace("* VID ","").replace("\n","")

            new_data.append('<div class="row mt-3">\n')
            new_data.append('    <div class="col-sm mt-3 mt-md-0">\n')
            new_data.append('        {% include video.liquid path="assets/video/'+line_vid+'.mp4" class="img-fluid rounded z-depth-1" controls=true %}\n')
            new_data.append('    </div>\n')
            new_data.append('</div>\n')
        else:
            # add rest of file to new_data list for later
            new_data.append(line)

with open(post_to_process.replace(".md","_new.md"),"w") as f:
    f.writelines(new_data)
#for line in new_data:
#    print(line)

