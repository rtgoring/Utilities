import os
import xml.etree.ElementTree as ET
import shutil

"""
Moves objects from parent folder
to location specified in text folder
"""

parentFolder = '/home/goring/Documents/alex/darknet/devkit/skynet5'
text_files = ['train_annot.txt', 'train_image.txt', 'valid_annot.txt', 'valid_image.txt']


for textFileName in text_files:
    destinationFolder = os.path.join(parentFolder, textFileName.split('.')[0])

    try:
        os.mkdir(destinationFolder)
    except:
        pass  # Already there
    file_opener = open(os.path.join(parentFolder, textFileName), 'r')

    for line in file_opener:
        print line
        line = line.split('\n')[0]
        shutil.copy(line, os.path.join(parentFolder, destinationFolder))
