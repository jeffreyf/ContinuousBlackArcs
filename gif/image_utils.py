# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:30:32 2018


"""

import re
import imageio
from os import listdir


def convert_folder_to_gif(folder, output_folder, output_name, end_delays=0):
    """
    Converts all the pngs in folder into a gif saved as output_name in the
    output_folder. end_delays determines how many times to repeat the first
    and final image in the folder
    
    """
    if not output_name.endswith(".gif"):
        output_name = output_name + ".gif"
    
    if not output_folder.endswith("/"):
        output_folder = output_folder + "/"
    
    if not folder.endswith("/"):
        folder = folder + "/"
    
    files = listdir(folder)
    files.sort(key=natural_keys)    
    
    # See: https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
    images = []
    
    # Read in the image data
    for file in files:
        images.append(imageio.imread(folder + file))
    
    # Repeat the beginnnings/ends
    for i in range(end_delays):
        # There's very likely a way easier pythonic way to do this with index scripting...
        images.append(images[-1])
        images.insert(0, images[0])
    
    imageio.mimsave(output_folder + output_name, images)
    

""" @author: https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside/5967539#5967539 """
def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]

if __name__ == "__main__":
    convert_folder_to_gif("staging",".", "optimization_run.gif")
