import csv
import os
import xml.etree.ElementTree as ET


def parse_annotation(path, file):
    """
    Function to parse XML files and return dict
      :return: Dictionary containing content counters of XMLFile
    """

    localdict = {}
    in_file = open(path + '/' + file)
    tree = ET.parse(in_file)
    root = tree.getroot()

    localdict['filePath'] = path
    localdict['fileName'] = file

    for obj in root.iter('object'):
        cls = obj.find('name').text

        # Add each class to allClasses if not present
        if cls not in allClasses:
            allClasses.append(cls)

        # Count number of times that class is in XML file
        if cls in localdict:
            localdict[cls] = localdict[cls] + 1
        else:
            localdict[cls] = 1
    return localdict


if __name__ == "__main__":
    # ###############
    # Editable Params
    # ###############

    directory = '/home/goring/Documents/DataSets/Sub/2017/Forward'
    CSVFILENAME = directory.split('/')[-1]  # last folder in directory path, could be anything

    allClasses = []  # Global to keep track of all annotated classes
    dictArray = []  # Global to keep all returned dicts - Contains entry for each XML file
    folderDicts = []  # Reduces dict array to one dict per folder

    allImages = 0  # Global to keep track of number of annotated image - One XML file for each image

    # Get listing of all annotation directories
    if os.path.isdir(directory):
        dirToAnnots = []  # Directories that contain annotations
        for a in os.listdir(directory):
            annotationDir = os.path.join(directory, a, 'Annotations')
            if os.path.isdir(annotationDir):  # Ensures folder exits
                dirToAnnots.append(annotationDir)

    # Creates Dict for each annotation
    for b in dirToAnnots:  # For each folder
        for c in os.listdir(b):  # For each annotation
            retDict = parse_annotation(b, c)
            dictArray.append(retDict)

    # Creates Dict for each Folder
    for dTA in dirToAnnots:  # For each folder
        folderDict = {}
        folderDict['filePath'] = dTA
        folderDict['Annotated Images'] = len(os.listdir(dTA))
        allImages = allImages + len(os.listdir(dTA))

        # Initializes counter for each key
        for q in allClasses:
            folderDict[q] = 0

        # Initializes counter for key
        folderDict['Total Annotations'] = 0

        for dA in dictArray:  # For each dict

            for dAA in dA:  # For each entry in dict
                if dAA in allClasses and dA['filePath'] == dTA:  # If current class and directory
                    folderDict[dAA] = folderDict[dAA] + 1  # Increment counters
                    folderDict['Total Annotations'] = folderDict['Total Annotations'] + 1
        folderDicts.append(folderDict)

    # creates dict with totals
    lastRowSummary = {}
    totalCounter = 0
    for c in allClasses:
        counter = 0
        for d in folderDicts:
            counter = counter + d[c]
        totalCounter = totalCounter + counter
        lastRowSummary[c] = counter

    lastRowSummary['Annotated Images'] = allImages
    lastRowSummary['Total Annotations'] = totalCounter
    lastRowSummary['filePath'] = 'Total Annotations'
    folderDicts.append(lastRowSummary)

    # Write to CSV file
    with open(CSVFILENAME + '.csv', 'w') as csvfile:

        # Organize headers in correct order
        rowheaders = ['filePath']
        allClasses.sort()
        for c in allClasses:
            rowheaders.append(c)
        rowheaders.append('Total Annotations')
        rowheaders.append('Annotated Images')

        filewriter = csv.DictWriter(csvfile, fieldnames=rowheaders)
        filewriter.writeheader()

        for row in folderDicts:
            filewriter.writerow(row)
