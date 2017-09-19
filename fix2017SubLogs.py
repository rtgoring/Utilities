import os

'''
When 2017 images were recorded a bug was in the file naming.
Files were named in the format: Year|DayOfYear|Hour|Minute|Second|.JPEG (Irrelevant to this issue)
Note: TX1's don't have RTC Batteries, so groundhog day... (Also Irrelevant to this issue)
ABC order for numbers though produces the following (wrong) order.

1
10
11
12
2
20
21
22

If loading images with python, images.sort() recreates this, however
images.sort(key=lambda f: int(filter(str.isdigit, f))) fixes it.

This script renames all images by padding the left digit, which fixes the issue. I.e

01
02 
10
11

This should be run so that the playback of the data is in the correct order. It may take a while.
'''

"""
Usage set directory_path as the path to the folder containing the images to be renamed.
It will search for a matching annotation, and rename that as well. 
"""

directory_path = '/home/goring/Documents/DataSets/Sub/2017/Forward'
parent_directories = []

if os.path.isdir(directory_path):
    for f in os.listdir(directory_path):
        if os.path.isdir(os.path.join(directory_path, f)):
            parent_directories.append(os.path.join(directory_path, f))

parent_directories.sort(key=lambda f: int(filter(str.isdigit, f)))
directory_counter = 0

for directory in parent_directories:
    if os.path.isdir(directory):
        images = []
        for a in os.listdir(directory):
            if a != 'Annotations':
                images.append(a)

    images.sort(key=lambda f: int(filter(str.isdigit, f)))

    maxLen = 0
    for image in images:
        if len(image) > maxLen:
            maxLen = len(image)

    for image in images:
        withoutExt = image.split('.')
        newImageName = str(directory_counter).zfill(2) + withoutExt[0].ljust(maxLen - len(withoutExt[1]) - 1, '0') + '.' + withoutExt[1]
        print image + " --> " + newImageName
        annotation = withoutExt[0] + '.xml'
        newAnnotationName = str(directory_counter).zfill(2) + withoutExt[0].ljust(maxLen - len(withoutExt[1]) - 1, '0') + '.xml'
        print annotation + "  --> " + newAnnotationName

        os.rename(os.path.join(directory, image), os.path.join(directory, newImageName))

        if os.path.isfile(os.path.join(directory, 'Annotations', annotation)):
            os.rename(os.path.join(directory,'Annotations', annotation), os.path.join(directory, 'Annotations', newAnnotationName))
    directory_counter +=1
print "DONE!"