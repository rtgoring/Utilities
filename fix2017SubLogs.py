import os
import cv2

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
