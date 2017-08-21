import os
import xml.etree.ElementTree as ET
import shutil

"""
Moves objects from parent folder
to location specified in text folder
"""

parentFolder = '/home/goring/Documents/alex/darknet/devkit/skynet4'
textFileName = 'trainImages.txt'

destinationFolder = os.path.join(parentFolder, textFileName.split('.')[0])

try:
    os.mkdir(destinationFolder)
except:
    pass  # Already there

file = open(os.path.join(parentFolder, textFileName), 'r')

for line in file:
    print line
    line = line.split('\n')[0]
    shutil.copy(line, os.path.join(parentFolder, destinationFolder))
