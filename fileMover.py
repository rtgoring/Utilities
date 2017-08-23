import os
import xml.etree.ElementTree as ET
import shutil

"""
Moves objects from parent folder
to location specified in text folder
"""

parent_folder = '/home/goring/Documents/alex/darknet/devkit/skynet2000'
text_files = ['train_annot.txt', 'train_image.txt', 'valid_annot.txt', 'valid_image.txt']

counter = 1
for f in text_files:  # For each file
    destination_folder = os.path.join(parent_folder, f.split('.')[0])

    try:
        os.mkdir(destination_folder)
    except:
        pass  # Already there

    file_reader = open(os.path.join(parent_folder, f), 'r')

    for line in file_reader:  # For each line
        line = line.split('\n')[0]  # Read line
        shutil.copy(line, os.path.join(parent_folder, destination_folder))  # Copy from location to new folder
    print counter
    counter = counter + 1

print "Done!"
