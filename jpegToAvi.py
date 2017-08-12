import numpy as np
import Tkinter, tkFileDialog
import cv2
import os
import sys


"""
Global Editable Parameters
"""
FPS = 15 # Ajusts playback speed
outputExt = '.avi' # .MP4 also works
imageFileTypes = ('jpg','jpeg')
directoriesToExclude = ('Annotations', 'annotations')

#Tkinter Initialize
root = Tkinter.Tk()
root.withdraw() #Hide Window


def getResolution(imagePath):
    """ Returns Resolution of an image
    Args:
		imagePath: A File path to load
    Returns:
		- A tuple of width and height
		- None if no image is loaded
    """
    sampleImage = cv2.imread(imagePath)
    if len(sampleImage):
        height = np.size(sampleImage, 0)
        width = np.size(sampleImage, 1)
        return (width, height)
    else:
		return None


def getCodex():
    """ Returns the Codex used to encode video
    
    Different systems have differnt codex installed.
    You may wish to edit or change depending on needs
    
    Args:
		None
    Returns:
		int of cv2 FOURCC type
    """
    if os.name =='posix': # OSX or Linux
        return cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    elif os.name =='nt': # Windows
        return cv2.cv.CV_FOURCC(*'XVID')


def main():
    """ This script is used to load a folder, or series of folders,
        containing sequential same sized images. An AVI is created
        in the root directory with the sub folders name.
    """
    inputDirectory = tkFileDialog.askdirectory(parent=root, initialdir=os.getcwd, title='Please select a directory')
    # Determines if inputDirectory is composed of folders or images
    if inputDirectory and os.path.isdir(inputDirectory):
        parentDirectories = []
        folderCount = 0
        imageCount = 0
        for f in os.listdir(inputDirectory):
            if os.path.isdir(os.path.join(inputDirectory, f)) and f not in directoriesToExclude: # Makes array of directories
                parentDirectories.append(os.path.join(inputDirectory, f))
    else:
        print "Not a valid path.\nExiting."
        sys.exit()

    if len(parentDirectories) ==0: ## No subfolders found, use only input directory
        parentDirectories.append(inputDirectory) 

    fourcc = getCodex()

    # Directories with images
    globalCounter = 0
    for pD in parentDirectories:
        allImages = []
        localCounter = 1
        globalCounter = globalCounter+1

        print "\n\nReading: " + str(pD) +"\n"
        
        # Gets all image names in Directory
        for f in os.listdir(pD):
            if f.endswith(imageFileTypes): # Checks file type
                allImages.append(os.path.join(pD, f))
        
        if len(allImages) > 0: # If images are found
	    imageResolution = getResolution(os.path.join(inputDirectory, allImages[0]))
	    print "saving to: " + os.path.join(inputDirectory, pD) + outputExt
            out = cv2.VideoWriter(os.path.join(inputDirectory, pD) + outputExt, fourcc, FPS, imageResolution)
        else:
            print "No Images found.\nSkipping Directory."
            continue # Exit current 'for' loop

        # Sorts all Images
        allImages.sort(key=lambda f: int(filter(str.isdigit, f)))
	
	# Once all images are sorted read through them and write them to file
        for image in allImages:
            frame = cv2.imread(os.path.join(inputDirectory,image))
            try:
                out.write(frame)
            except:
                print "Can't Write"
            print ("%d/%d: %d of %d") % (globalCounter, len(parentDirectories), localCounter, len(allImages))
            localCounter = localCounter+1


if __name__ == '__main__':
    main()
