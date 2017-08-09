import numpy as np
import Tkinter, tkFileDialog
import cv2
import os
import sys

FPS = 15
RESOLUTION = (1920,1200)
outputExt = '.avi'

# Define the codec and create VideoWriter object
if os.name =='posix': ## MAC
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
elif os.name =='nt': ## WINDOWS
    fourcc = cv2.cv.CV_FOURCC(*'XVID')

root = Tkinter.Tk()
root.withdraw()

inputDirectory = None
inputDirectory = tkFileDialog.askdirectory(parent=root, initialdir=os.getcwd, title='Please select a directory')

def main():
    ## Determines if inputDirectory is composed of folders or images
    if os.path.isdir(inputDirectory):
        parentDirectories = []
        folderCount = 0
        imageCount = 0
        for f in os.listdir(inputDirectory):
            if os.path.isdir(os.path.join(inputDirectory,f))and f != 'Annotations' : #Makes array of directories
                parentDirectories.append(os.path.join(inputDirectory,f))
    else:
        print "exiting"
        sys.exit()

    if len(parentDirectories) ==0: ## No subfolders found, must just be images
        parentDirectories.append(inputDirectory)


    #Directories with images
    globalCounter = 0
    for dir in parentDirectories:
        allImages = []
        localCounter = 1
        globalCounter = globalCounter+1

        print "\n\nReading: " + str(dir) +"\n"
        #Gets all Images in Directory
        for f in os.listdir(dir):
            if f.endswith('.jpg') or f.endswith('.jpeg'):
                allImages.append(os.path.join(dir,f))
        if len(allImages) > 0: #Gets Resolution of 1st image, assume all are same
            sampleImage = cv2.imread(os.path.join(inputDirectory,allImages[0]))
            height = np.size(sampleImage, 0)
            width = np.size(sampleImage, 1)
            RESOLUTION = (width,height)
            out = cv2.VideoWriter(os.path.join(inputDirectory,dir)+outputExt,fourcc, FPS, RESOLUTION)
        else:
            print "No Images found. Skipping..."
            continue

        # Sorts all Images
        allImages.sort(key=lambda f: int(filter(str.isdigit, f)))

        for image in allImages:
            frame = cv2.imread(os.path.join(inputDirectory,image))
            try:
                out.write(frame)
            except:
                print "Can't Write"
            print ("%d/%d: %d of %d") % (globalCounter,len(parentDirectories),localCounter, len(allImages))
            localCounter = localCounter+1



if __name__ == '__main__':
    main()
