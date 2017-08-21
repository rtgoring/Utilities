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
import shutil

HomeDirectory = '/home/goring/Documents/alex/darknet/devkit/skynet4/'
AnnotationDirectory = '/home/goring/Documents/alex/darknet/devkit/skynet4/Annotations'
ImageDirectory = '/home/goring/Documents/alex/darknet/devkit/skynet4/JPEGImages'
outAnnotations = 'GateAnnotationsXML'
outImages = 'GateImages'

try:
    os.mkdir(os.path.join(HomeDirectory, outImages))
except:
    pass  # already there
try:
    os.mkdir(os.path.join(HomeDirectory, outAnnotations))
except:
    pass  # Already there

targetClass = 'gate'
VOCAnnotations = []
for f in os.listdir(AnnotationDirectory):
    if f.endswith('.xml'):  # Checks file type
        VOCAnnotations.append(f)

annotationsToMove = []
print "reading " + str(len(VOCAnnotations)) + " files"
counter = 0
totAnnots = str(len(VOCAnnotations))
for f in VOCAnnotations:
    in_file = open(os.path.join(AnnotationDirectory, f))
    tree = ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls == targetClass:
            annotationsToMove.append(f)

    counter = counter + 1
    print str(counter) + "/" + totAnnots
print "Found " + str(len(annotationsToMove)) + " instances of " + targetClass
# shutil.copy(JPEGImagesFileNamePath, JPEGImagesFileNamePathFinal)

counter = 0
totAnnots = str(len(annotationsToMove))
failedA = []
failedI = []

out_fileImages = open(os.path.join(HomeDirectory, "trainImages.txt"), 'w')
out_fileAnnots = open(os.path.join(HomeDirectory, "trainAnnots.txt"), 'w')

for f in annotationsToMove:
    f2 = f.split('.')[0] + '.jpeg'  # xml -> txt
    try:
        # shutil.copy(os.path.join(AnnotationDirectory,f), os.path.join(HomeDirectory,outAnnotations,f))
        out_fileImages.write("%s/%s\n" % (ImageDirectory, f2))
    except:
        failedA.append(f)
    try:
        out_fileAnnots.write("%s/%s\n" % (AnnotationDirectory, f))
        # shutil.copy(os.path.join(ImageDirectory,f2), os.path.join(HomeDirectory,outImages,f2))
    except:
        failedI.append(f2)

    print str(counter) + "/" + totAnnots
    counter = counter + 1
print "DONE\n\n\n"

for f in failedA:
    print f

for f in failedI:
    print f
