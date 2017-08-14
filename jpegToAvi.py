import Tkinter
import numpy as np
import os
import sys
import tkFileDialog

import cv2

"""
Global Editable Parameters
"""
FPS = 15  # Adjusts playback speed
outputExt = '.avi'  # .MP4 also works
imageFileTypes = ('jpg', 'jpeg')
directoriesToExclude = ('Annotations', 'annotations')

# Tkinter Initialize
root = Tkinter.Tk()
root.withdraw()  # Hide Window


def getResolution(imagePath):
    """ Returns Resolution of an image
    Args:
        - imagePath: A File path to load
    Returns:
        - A tuple of width and height
        - None if no image is loaded
    """
    sample_image = cv2.imread(imagePath)
    if len(sample_image):
        height = np.size(sample_image, 0)
        width = np.size(sample_image, 1)
        return width, height
    else:
        return None


def getCodex():
    """ Returns the Codex used to encode video

    Different systems have differnt codex installed.
    You may wish to edit or change depending on needs

    Args:
        - None
    Returns:
        - int of cv2 FOURCC type
    """
    if os.name == 'posix':  # OSX or Linux
        return cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    elif os.name == 'nt':  # Windows
        return cv2.cv.CV_FOURCC(*'XVID')


def main():
    """ This script is used to load a folder, or series of folders,
        containing sequential same sized images. An AVI is created
        in the root DATA_DIRECTORY with the sub folders name.
    """
    inputDirectory = tkFileDialog.askdirectory(parent=root, initialdir=os.getcwd,
                                               title='Please select a DATA_DIRECTORY')
    # Determines if inputDirectory is composed of folders or images
    if inputDirectory and os.path.isdir(inputDirectory):
        parent_directories = []
        for f in os.listdir(inputDirectory):
            if os.path.isdir(
                    os.path.join(inputDirectory, f)) and f not in directoriesToExclude:  # Makes array of directories
                parent_directories.append(os.path.join(inputDirectory, f))
    else:
        print "Not a valid path.\nExiting."
        sys.exit()

    if len(parent_directories) == 0:  ## No subfolders found, use only input DATA_DIRECTORY
        parent_directories.append(inputDirectory)

    fourcc = getCodex()

    # Directories with images
    global_counter = 0
    for pD in parent_directories:
        all_images = []
        local_counter = 1
        global_counter = global_counter + 1

        print "\n\nReading: " + str(pD) + "\n"

        # Gets all image names in Directory
        for f in os.listdir(pD):
            if f.endswith(imageFileTypes):  # Checks file type
                all_images.append(os.path.join(pD, f))

        if len(all_images) > 0:  # If images are found
            image_resolution = getResolution(os.path.join(inputDirectory, all_images[0]))
            print "saving to: " + os.path.join(inputDirectory, pD) + outputExt
            out = cv2.VideoWriter(os.path.join(inputDirectory, pD) + outputExt, fourcc, FPS, image_resolution)
        else:
            print "No Images found.\nSkipping Directory."
            continue  # Exit current loop

        # Sorts all Images
        all_images.sort(key=lambda f: int(filter(str.isdigit, f)))

        # Once all images are sorted read through them and write them to file
        for image in all_images:
            frame = cv2.imread(os.path.join(inputDirectory, image))
            try:
                out.write(frame)
            except:
                print "Can't Write"
            print ("%d/%d: %d of %d") % (global_counter, len(parent_directories), local_counter, len(all_images))
            local_counter = local_counter + 1


if __name__ == '__main__':
    main()
