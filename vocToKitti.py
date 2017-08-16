"""
Digits uses KITTI format

#Values    Name      Description
----------------------------------------------------------------------------
   1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                     truncated refers to the object leaving image boundaries
   1    occluded     Integer (0,1,2,3) indicating occlusion state:
                     0 = fully visible, 1 = partly occluded
                     2 = largely occluded, 3 = unknown
   1    alpha        Observation angle of object, ranging [-pi..pi]
   4    bbox         2D bounding box of object in the image (0-based index):
                     contains left, top, right, bottom pixel coordinates
   3    dimensions   3D object dimensions: height, width, length (in meters)
   3    location     3D object location x,y,z in camera coordinates (in meters)
   1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
   1    score        Only for results: Float, indicating confidence in
                     detection, needed for p/r curves, higher is better.


Karlsruhe Institute of Technology recomends VOD-converter, but it's shit and broke. Therefor this is my even
more broke attempt. But it works.
https://github.com/umautobots/vod-converter
"""

import os
import xml.etree.ElementTree as ET

parentDirectory = '/home/goring/Documents/DataSets/Sub/2017/Forward/2015TransdecData/'

VOCDirectory = os.path.join(parentDirectory, 'Annotations')
KITTIDirectory = os.path.join(parentDirectory, 'KITTIAnnotations')
try:
    os.mkdir(KITTIDirectory)
except:
    pass  # Already exists

VOCAnnotations = []
for f in os.listdir(VOCDirectory):
    if f.endswith('.xml'):  # Checks file type
        VOCAnnotations.append(f)

for f in VOCAnnotations:
    fTXT = f.split('.')[0] + '.txt'
    in_file = open(os.path.join(VOCDirectory, f))
    out_file = open(os.path.join(KITTIDirectory, fTXT), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        cls = obj.find('name').text
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))  # left, right, top, bottom
        out_file.write(
            "%s 0 0 0 %d %d %d %d 0 0 0 0 0 0 0\n" % (cls, b[0], b[2], b[1], b[3]))  # left, top, right, bottom
print "Done. %d Converted." % len(VOCAnnotations)
