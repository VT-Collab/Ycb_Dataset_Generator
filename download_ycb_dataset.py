#Copyright 2015 Yale University - Grablab
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Modified to work with Python 3 by Sebastian Castro, 2020

import os
import sys
import json
import shutil
import urllib
import inspect
from urllib.request import Request, urlopen


# Define an output folder
output_directory = os.path.join("models", "ycb")
models_folder_location = f'{os.getcwd()}/models'  

# Define a list of objects to download from
# http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/

one_object = ["001_chips_can"]

two_objects = ["004_sugar_box", 
                "001_chips_can"]

four_Objects = ["011_banana", 
                "002_master_chef_can",
                "003_cracker_box",
                "004_sugar_box"]

more_objects = ["001_chips_can", 
                "002_master_chef_can",
                "003_cracker_box",
                "004_sugar_box", 
                "005_tomato_soup_can",
                "006_mustard_bottle",
                "007_tuna_fish_can",
                "008_pudding_box",
                "009_gelatin_box",
                "035_power_drill",
                "036_wood_block",
                "037_scissors",
                "038_padlock"]

# all = [
#     "001_chips_can",
#     "002_master_chef_can",
#     "003_cracker_box",
#     "004_sugar_box",
#     "005_tomato_soup_can",
#     "006_mustard_bottle",
#     "007_tuna_fish_can",
#     "008_pudding_box",
#     "009_gelatin_box",
#     "010_potted_meat_can",
#     "011_banana",
#     "012_strawberry",
#     "013_apple",
#     "014_lemon",
#     "015_peach",
#     "016_pear",
#     "017_orange",
#     "018_plum",
#     "019_pitcher_base",
#     "021_bleach_cleanser",
#     "022_windex_bottle",
#     "023_wine_glass",
#     "024_bowl",
#     "025_mug",
#     "026_sponge",
#     "027-skillet",
#     "028_skillet_lid",
#     "029_plate",
#     "030_fork",
#     "031_spoon",
#     "032_knife",
#     "033_spatula",
#     "035_power_drill",
#     "036_wood_block",
#     "037_scissors",
#     "038_padlock",
#     "039_key",
#     "040_large_marker",
#     "041_small_marker",
#     "042_adjustable_wrench",
#     "043_phillips_screwdriver",
#     "044_flat_screwdriver",
#     "046_plastic_bolt",
#     "047_plastic_nut",
#     "048_hammer",
#     "049_small_clamp",
#     "050_medium_clamp",
#     "051_large_clamp",
#     "052_extra_large_clamp",
#     "053_mini_soccer_ball",
#     "054_softball",
#     "055_baseball",
#     "056_tennis_ball",
#     "057_racquetball",
#     "058_golf_ball",
#     "059_chain",
#     "061_foam_brick",
#     "062_dice",
#     "063-a_marbles",
#     "063-b_marbles",
#     "063-c_marbles",
#     "063-d_marbles",
#     "063-e_marbles",
#     "063-f_marbles",
#     "065-a_cups",
#     "065-b_cups",
#     "065-c_cups",
#     "065-d_cups",
#     "065-e_cups",
#     "065-f_cups",
#     "065-g_cups",
#     "065-h_cups",
#     "065-i_cups",
#     "065-j_cups",
#     "070-a_colored_wood_blocks",
#     "070-b_colored_wood_blocks",
#     "071_nine_hole_peg_test",
#     "072-a_toy_airplane",
#     "072-b_toy_airplane",
#     "072-c_toy_airplane",
#     "072-d_toy_airplane",
#     "072-e_toy_airplane",
#     "072-f_toy_airplane",
#     "072-g_toy_airplane",
#     "072-h_toy_airplane",
#     "072-i_toy_airplane",
#     "072-j_toy_airplane",
#     "072-k_toy_airplane",
#     "073-a_lego_duplo",
#     "073-b_lego_duplo",
#     "073-c_lego_duplo",
#     "073-d_lego_duplo",
#     "073-e_lego_duplo",
#     "073-f_lego_duplo",
#     "073-g_lego_duplo",
#     "073-h_lego_duplo",
#     "073-i_lego_duplo",
#     "073-j_lego_duplo",
#     "073-k_lego_duplo",
#     "073-l_lego_duplo",
#     "073-m_lego_duplo",
#     "076_timer",
#     "077_rubiks_cube"
#   ]

# print(objects_to_download)
# exit(0)

# objects_to_download = ["001_chips_can", 
#                        "002_master_chef_can",
#                        "003_cracker_box",
#                        "004_sugar_box"]

# You can edit this list to only download certain kinds of files.
# 'berkeley_rgbd' contains all of the depth maps and images from the Carmines.
# 'berkeley_rgb_highres' contains all of the high-res images from the Canon cameras.
# 'berkeley_processed' contains all of the segmented point clouds and textured meshes.
# 'google_16k' contains google meshes with 16k vertices.
# 'google_64k' contains google meshes with 64k vertices.
# 'google_512k' contains google meshes with 512k vertices.
# See the website for more details.
#files_to_download = ["berkeley_rgbd", "berkeley_rgb_highres", "berkeley_processed", "google_16k", "google_64k", "google_512k"]
files_to_download = ["berkeley_rgb_highres"]

# Extract all files from the downloaded .tgz, and remove .tgz files.
# If false, will just download all .tgz files to output_directory
extract = True

base_url = "http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/data/"
objects_url = "https://ycb-benchmarks.s3.amazonaws.com/data/objects.json"

def fetch_objects(url):
    """ Fetches the object information before download """
    response = urlopen(url)
    html = response.read()
    objects = json.loads(html)
    return objects["objects"]


def download_file(url, filename):
    """ Downloads files from a given URL """
    u = urlopen(url)
    f = open(filename,"wb")
    file_size = int(u.getheader("Content-Length"))    
    print("Downloading: {} ({} MB)".format(filename, file_size/1000000.0))

    file_size_dl = 0
    block_sz = 65536
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl/1000000.0, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status)
    f.close()
    

def tgz_url(object, type):
    """ Get the TGZ file URL for a particular object and dataset type """
    if type in ["berkeley_rgbd", "berkeley_rgb_highres"]:
        return base_url + "berkeley/{object}/{object}_{type}.tgz".format(object=object,type=type)
    elif type in ["berkeley_processed"]:
        return base_url + "berkeley/{object}/{object}_berkeley_meshes.tgz".format(object=object,type=type)
    else:
        return base_url + "google/{object}_{type}.tgz".format(object=object,type=type)


def extract_tgz(filename, dir):
    """ Extract a TGZ file """
    tar_command = "tar -xzf {filename} -C {dir}".format(filename=filename,dir=dir)
    os.system(tar_command)
    os.remove(filename)

def check_url(url):
    """ Check the validity of a URL """
    try:
        request = Request(url)
        request.get_method = lambda : 'HEAD'
        response = urlopen(request)
        return True
    except Exception as e:
        return False

def main():
    user_input = int(input(inspect.cleandoc("Choose:\n\t\
        1 => 1 object\n\t\
        2 => 2 objects\n\t\
        4 => 4 objects\n\t\
        13 => 13 objects\n\t\
        911 => all objects\n\n\
        Your Response:\t")))

    if(user_input == 1):
        objects_to_download = one_object
    elif (user_input == 2):
        objects_to_download = two_objects
    elif(user_input == 4):
        objects_to_download = four_Objects
    elif(user_input == 13):
        objects_to_download = more_objects
    elif(user_input == 911):
        objects_to_download = "all"

    # Remove Models Folder:
    if(os.path.exists(models_folder_location)):
        shutil.rmtree(models_folder_location)
    os.makedirs(output_directory)

    # Grab all the object information
    objects = fetch_objects(objects_url)

    # Download each object for all objects and types specified
    for object in objects:
        if objects_to_download == "all" or object in objects_to_download:
            for file_type in files_to_download:
                url = tgz_url(object, file_type)
                if not check_url(url):
                    continue
                filename = "{path}/{object}_{file_type}.tgz".format(
                    path=output_directory,
                    object=object,
                    file_type=file_type)
                download_file(url, filename)
                if extract:
                    extract_tgz(filename, output_directory)

if __name__ == "__main__":
    main()