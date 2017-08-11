import os

'''
When 2017 images were recorded a bug was in the filenaming.
Files were named in the format: Year|DayOfYear|Hour|Minute|Second|.JPEG (Irelevant to this issue)
Note: TX1's don't have RTC Batteries, so groundhog day... (Also irelevant to this issue)
ABC order for numbers though produces the following (wrong) order.

1
10
11
12
2
20
21
22

If loading images with python images.sort() recreates this, however
images.sort(key=lambda f: int(filter(str.isdigit, f))) fixes it.

This script renames all images by pading the left digit, which fixes the issue. I.e

01
02 
10
11


Note: If you rename an annotated image, rename the annotation.
This script will do this :)
'''

'''
Usage set dectory as the path to the folder containing the images to be renamed.
'''


directory = 'test'

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

counter = 0
for image in images:
    withoutExt = image.split('.')
    newImageName = withoutExt[0].ljust(maxLen-len(withoutExt[1]) -1, '0') + '.'+withoutExt[1]
    print image + " --> " + newImageName
    os.rename(os.path.join(directory,image), os.path.join(directory,newImageName))
