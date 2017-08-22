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

target_class = 'gate'
voc_annotations = []
for f in os.listdir(AnnotationDirectory):
    if f.endswith('.xml'):  # Checks file type
        voc_annotations.append(f)

annotations_to_move = []
print "reading " + str(len(voc_annotations)) + " files"
counter = 1
total_annotations = str(len(voc_annotations))
for f in voc_annotations:
    in_file = open(os.path.join(AnnotationDirectory, f))
    tree = ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls == target_class:
            annotations_to_move.append(f)

    counter = counter + 1
    print str(counter) + "/" + total_annotations
print "Found " + str(len(annotations_to_move)) + " instances of " + target_class

counter = 1
total_annotations = str(len(annotations_to_move))
failed_annotations = []
failed_images = []

out_fileImages = open(os.path.join(HomeDirectory, "trainImages.txt"), 'w')
out_fileAnnots = open(os.path.join(HomeDirectory, "trainAnnots.txt"), 'w')

for f in annotations_to_move:
    f2 = f.split('.')[0] + '.jpeg'  # xml -> txt
    try:
        shutil.copy(os.path.join(AnnotationDirectory,f), os.path.join(HomeDirectory,outAnnotations,f))
        out_fileImages.write("%s/%s\n" % (ImageDirectory, f2))
    except:
        failed_annotations.append(f)
    try:
        out_fileAnnots.write("%s/%s\n" % (AnnotationDirectory, f))
        shutil.copy(os.path.join(ImageDirectory,f2), os.path.join(HomeDirectory,outImages,f2))
    except:
        failed_images.append(f2)

    print str(counter) + "/" + total_annotations
    counter = counter + 1
print "DONE\n\n\n"

for f in failed_annotations:
    print f

for f in failed_images:
    print f
