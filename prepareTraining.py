import os
from os import getcwd
import shutil
import xml.etree.ElementTree as ET

# ###################
# Global Parameters
# ###################
CPP = False
parentPath = '/home/goring/Documents/DataSets/Sub/2017/Forward/'
darknetPath = '/home/goring/Documents/alex/darknet'
EXTENSION = '.jpeg'
datasetName = 'skynet5'
classes = sorted(['gate', 'redbuoy', 'yellowbuoy', 'greenbuoy', 'path', 'gateinv'])
CFGModel = 'tiny-yolo-voc'  # 'yolo-voc.2.0' # 'tiny-yolo-voc'


# detector.C 133 - How often to save snapshots


def convert(size, box):
    """
    Converts Bounding boxes to ratios
    :param size:
    :param box:
    :return:
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(year, image_id):
    """
    Function to convert XML annotations to TXT Labels
    :param year:
    :param image_id:
    :return:
    """
    in_file = open('devkit/%s/Annotations/%s.xml' % (year, image_id))
    out_file = open('devkit/%s/labels/%s.txt' % (year, image_id), 'w')
    localAnnotations = 0
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in foundClasses:
            foundClasses.append(cls)
        if cls not in classes or int(difficult) == 1:
            if cls not in ignoredClasses:
                ignoredClasses.append(cls)
            continue
        cls_id = classes.index(cls)
        cls_tracker[cls_id] = cls
        classCounter[cls_id] = classCounter[cls_id] + 1
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        localAnnotations = localAnnotations + 1
    return localAnnotations


def convertXMLToLabels():
    """
       Converts XML files to Labels
       Returns
          - Number of objects that were annotated
    """
    annotatedItemsLocal = 0
    for year, image_set in sets:
        if not os.path.exists('devkit/%s/labels/' % (year)):
            os.makedirs('devkit/%s/labels/' % (year))
        image_ids = open('devkit/%s/ImageSets/Main/%s.txt' % (year, image_set)).read().strip().split()
        list_file = open(datasetName + '/%s_%s.txt' % (year, image_set), 'w')
        for image_id in image_ids:
            list_file.write('%s/devkit/%s/JPEGImages/%s%s\n' % (wd, year, image_id, EXTENSION))
            # print ('%s/devkit/%s/JPEGImages/%s%s\n'%(wd, year, image_id,EXTENSION))
            annotatedItemsLocal = annotatedItemsLocal + convert_annotation(year, image_id)

        list_file.close()
        return annotatedItemsLocal


def copyLabels():
    """
    Copies the data/names folder

    Inorder to print text to image, individual letters are loaded. These are hard paths to /data/labels.
    Therefor, it is required to move them to the local DATA_DIRECTORY.
    """

    try:
        shutil.copytree(os.path.join(wd, 'data', 'labels'), os.path.join(datasetName, 'data', 'labels'))
    except:
        pass  # Already is there
    return True


def createDirectories(requiredDirectories):
    """
    Creates Directories in list
    :param requiredDirectories:
    :return:
    """
    for directory in requiredDirectories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def copyCFGFile():
    """
    Copies and Renames CFG Files
    :return:
    """
    try:
        shutil.copy(CFGFile, datasetName)
        os.rename(os.path.join(datasetName, CFGModel + '-' + str(len(classes)) + '.cfg'),
                  os.path.join(datasetName, datasetName + '.cfg'))
        return True
    except:
        return False


def createMetaDataFile():
    """
    Creates a txt file with metadata

    Returns
        - True if Success
        - False if Error
    """

    try:
        metaDataWriter = open(os.path.join(datasetName, "data.txt"), 'w')
    except:
        print "Cannot open MetaDataWriter"
        return False

    metaDataWriter.write("Trained Classes:\n")
    metaDataWriter.write(''.join(e + ', ' for e in sorted(classes))[:-2] + "\n\n")
    metaDataWriter.write("Classes Found in XML File:\n")
    metaDataWriter.write(''.join(e + ', ' for e in sorted(foundClasses))[:-2] + "\n\n")
    metaDataWriter.write("Copyable Classes Found in XML File:\n")
    metaDataWriter.write(''.join('\'' + e + '\'' + ', ' for e in sorted(foundClasses))[:-2] + "\n\n")
    metaDataWriter.write("Ignored Classes Found in XML File:\n")
    metaDataWriter.write(''.join(e + ', ' for e in sorted(ignoredClasses))[:-2] + "\n\n")
    metaDataWriter.write("CLS ID Order:\n")
    metaDataWriter.write(''.join(e + ', ' for e in cls_tracker)[:-2] + "\n\n")
    metaDataWriter.write("Number of each class Found in XML File:\n")
    metaDataWriter.write(''.join(str(e) + ', ' for e in classCounter)[:-2] + "\n\n")
    metaDataWriter.write("There are " + str(totalAnnotations) + " Annotated Images\n\n")
    metaDataWriter.write("There are " + str(annotatedItems) + " Annotated Items\n\n")
    metaDataWriter.write("There are " + str(copiedAnnotations) + " Copied Annotations\n\n")
    metaDataWriter.write("There are " + str(copiedImages) + " Copied Images\n\n")
    metaDataWriter.write("Training Script\n")
    metaDataWriter.write(
        "../darknet detector train " + datasetName + '.data ' + datasetName + '.cfg' + " ../darknet19_448.conv.23\n\n")
    metaDataWriter.write("Demo Script\n")
    metaDataWriter.write(
        "../darknet detector demo " + datasetName + ".data " + datasetName + ".cfg " + "Models/" + datasetName + "_900.weights ../aaa.mp4\n")
    metaDataWriter.close()
    return True


def createDemoScriptFile():
    # TODO Fix default weight for script
    # TODO Fix default video for script
    """
    Create a Script to Run a Demo

    Returns
        - True if Success
        - False if Error
    """

    try:
        demoScriptWriter = open(os.path.join(datasetName, datasetName + '_demo.sh'), 'w')
    except:  # Can't easily make two levels deep at once, could use string split though
        print "Cannot open demoScriptWriter"
        return False

    if CPP:
        demoScriptWriter.write(
            "../darknet-cpp detector demo " + datasetName + ".data " + datasetName + ".cfg " + "Models/" + datasetName + "_900.weights ../aaa.mp4\n")
    else:
        demoScriptWriter.write(
            "../darknet detector demo " + datasetName + ".data " + datasetName + ".cfg " + "Models/" + datasetName + "_900.weights ../aaa.mp4\n")

    demoScriptWriter.close()

    # Makes script executable
    try:
        os.chmod(os.path.join(datasetName, datasetName + '_demo.sh'), 0755)
    except:
        print "Cannot make run script executable"
        return False
    return True


def createTrainScriptFile():
    # TODO Configurable training weights param
    """
    Create a Script to train model

    Returns
        - True if Success
        - False if Error
    """

    try:
        trainingScriptWriter = open(os.path.join(datasetName, datasetName + '_train.sh'), 'w')
    except:  # Can't easily make two levels deep at once, could use string split though
        print "Can't open Names trainingScriptWriter"
        return False

    if CPP:
        trainingScriptWriter.write(
            "../darknet-cpp detector train " + datasetName + '.data ' + datasetName + '.cfg' + " ../darknet19_448.conv.23")
    else:
        trainingScriptWriter.write(
            "../darknet detector train " + datasetName + '.data ' + datasetName + '.cfg' + " ../darknet19_448.conv.23")
    trainingScriptWriter.close()

    # Makes script executable
    os.chmod(os.path.join(datasetName, datasetName + '_train.sh'), 0755)
    return True


def createDataFile():
    """
    Creates required .data file

    Returns
        - True if Success
        - False if Error
    """

    try:
        datafileWriter = open(os.path.join(datasetName, datasetName + '.data'), 'w')
    except:  # Can't easily make two levels deep at once, could use string split though
        print "Can't open Names datafileWriter"
        return False
    datafileWriter.write('classes= ' + str(len(classes)) + '\n')
    datafileWriter.write('train = ' + wd + '/' + datasetName + '/' + datasetName + '_' + sets[0][1] + '.txt' + '\n')
    datafileWriter.write('valid = /NeverActuallyWroteThisPartYetSoDoesntMatter.txt' + '\n')
    datafileWriter.write('names = ' + datasetName + '.names' + '\n')
    datafileWriter.write('backup = Models')
    datafileWriter.close()
    return True


def createNamesFile():
    """
    Create required .names file

    Returns
        - True if Success
        - False if Error
    """

    try:
        NamesfileWriter = open(os.path.join(datasetName, datasetName + '.names'), 'w')
    except:  # Can't easily make two levels deep at once, could use string split though
        print "Can't open Names fileWriter"
        return False

    for klass in classes:
        NamesfileWriter.write(klass + "\n")
    NamesfileWriter.close()
    return True


if __name__ == '__main__':
    # ###################
    # This script takes all of the annotations that were created, and copies them,
    # and their linked image to the proper location in yolo, as well as
    # creating the labels file
    # ###################

    CFGFile = os.path.join("cfg", CFGModel, CFGModel + '-' + str(len(classes)) + '.cfg')
    print "Preparing to train %s Classes.\nUsing Model: %s" % (
        str(len(classes)), CFGModel + '-' + str(len(classes)) + '.cfg')
    print "Dataset: " + datasetName
    print "Trained Classes: "
    print classes
    print "\n\n"
    classCounter = [0] * len(classes)  # Counts num Annots per class
    cls_tracker = [''] * len(classes)  # Verifies ClS IDs are in same order of classes
    foundClasses = []  # Contains classes found in XML files
    ignoredClasses = []  # Contains classes found in XML file that are not trained
    parentFolders = []
    totalAnnotations = 0  # Number of Annotations Files Found
    copiedAnnotations = 0  # Number of Annotations copied to working DATA_DIRECTORY
    copiedImages = 0  # Number of Images copied to working DATA_DIRECTORY

    #wd = getcwd()
    wd = darknetPath # Not been tested yet #TODO Test this
    os.chdir(darknetPath) #TODO Test th is too
    sets = [(datasetName, 'train')]
    finalParent = wd + '/devkit/' + sets[0][0]
    finalDestination = wd + '/devkit/' + sets[0][0] + '/Annotations'
    trainValLocation = wd + '/devkit/' + sets[0][0] + '/ImageSets/Main'

    requiredDirectories = [
        trainValLocation,
        finalDestination,
        datasetName,
        finalParent,
        datasetName + '/Models',
        finalParent + '/ImageSets',
        finalParent + '/JPEGImages'
    ]

    createDirectories(requiredDirectories)

    # Creates List of Folders containing images
    for f in os.listdir(parentPath):
        if ('.') not in f and f != 'Annotations' and f != 'Useless':  # Removes files and unwanted folders
            parentFolders.append(f)
            parentFolders = sorted(parentFolders)

    # ###################
    # Creates file listing training set of file names
    #
    # Assuming Structure:
    # -parentPath
    #    -Data1
    #       -ImageN.jpg
    #       -Annotations
    #       -Annotation.xml
    #
    # Goes through each folder in the parent path, and looks inside the internal Annotation folder.
    # Saves the names of each of the annotations, which indicate the used images.
    # Copy the annotation and image to devkit
    #
    # Purpose is to reduce the need of having all images in the dataset in the training set
    # ###################

    try:
        fileWriter = open(os.path.join(trainValLocation, 'train.txt'), 'w')
    except:
        print "Can't open fileWriter"

    # For each folder within root - this is where everything happens
    print "Copying. This may take a moment."
    for f in parentFolders:
        try:
            for fileName in os.listdir(os.path.join(parentPath, f, 'Annotations')):  # Go through each annotation
                # Write filename with no extension
                fileWriter.write(fileName[:-4] + "\n")

                # Prepare Annotation File Paths
                annotationFileName = fileName
                annotationFileNamePath = os.path.join(parentPath, f, 'Annotations', annotationFileName)

                # Prepare Image File Paths
                JPEGImagesFileName = fileName[:-4] + EXTENSION  # strips off .xml adds .jpg/.jpeg
                JPEGImagesFileNamePath = os.path.join(parentPath, f, JPEGImagesFileName)

                # Move Annotations
                # print "Moving: " + annotationFileNamePath + " to: " + annotationFileNamePathFinal
                annotationFileNamePathFinal = os.path.join(finalParent, "Annotations")
                try:
                    shutil.copy(annotationFileNamePath, annotationFileNamePathFinal)
                    copiedAnnotations = copiedAnnotations + 1
                except:
                    print "failed copying annotation" + annotationFileNamePath + " to: " + annotationFileNamePathFinal

                # Move Images
                JPEGImagesFileNamePathFinal = os.path.join(finalParent, "JPEGImages")
                #print "Moving: " + JPEGImagesFileNamePath + " to: " + JPEGImagesFileNamePathFinal
                try:
                    shutil.copy(JPEGImagesFileNamePath, JPEGImagesFileNamePathFinal)
                    copiedImages = copiedImages + 1
                except:
                    print "failed copying JPEGImages" + JPEGImagesFileNamePath + " to: " + JPEGImagesFileNamePathFinal
                totalAnnotations = totalAnnotations + 1

        except:
            pass
            # print 'No Annotation file in ' + parentPath + f
    fileWriter.close()

    copyCFGFile()
    copyLabels()
    annotatedItems = convertXMLToLabels()
    createMetaDataFile()
    createDemoScriptFile()
    createTrainScriptFile()
    createDataFile()
    createNamesFile()
    print "Done."
