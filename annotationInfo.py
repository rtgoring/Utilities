import os
import xml.etree.ElementTree as ET
import csv


def parse_annotation(path, file):
    """
    Function to parse XML files and return dict
      :return:
    """

    localDict = {}
    in_file = open(path + '/' + file)
    tree = ET.parse(in_file)
    root = tree.getroot()

    localDict['filePath'] = path
    localDict['fileName'] = file

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in allClasses:
            allClasses.append(cls)

        if cls in localDict:
            localDict[cls] = localDict[cls] + 1
        else:
            localDict[cls] = 1
    return localDict


if __name__ == "__main__":
    directory = '/home/goring/Documents/DataSets/Sub/2017/Forward'
    CSVFILENAME = directory.split('/')[-1]
    allClasses = []
    allImages = 0
    # Get listing of all annotation directories
    if os.path.isdir(directory):
        dirToAnnots = []
        for a in os.listdir(directory):
            annotationDir = os.path.join(directory, a, 'Annotations')
            if os.path.isdir(annotationDir):
                dirToAnnots.append(annotationDir)
    dictArray = []
    for b in dirToAnnots:
        for c in os.listdir(b):
            retDict = parse_annotation(b, c)
            dictArray.append(retDict)

    folderDicts = []
    for dTA in dirToAnnots:
        folderDict = {}
        folderDict['filePath'] = dTA
        folderDict['Annotated Images'] = len(os.listdir(dTA))
        allImages = allImages + len(os.listdir(dTA))
        for q in allClasses:
            folderDict[q] = 0

        folderDict['Total Annotations'] = 0
        for dA in dictArray:
            # print dA

            for dAA in dA:
                if dAA in allClasses and dA['filePath'] == dTA:
                    folderDict[dAA] = folderDict[dAA] + 1
                    folderDict['Total Annotations'] = folderDict['Total Annotations'] + 1
        folderDicts.append(folderDict)

    lastRowSummary = {}
    columns = allClasses
    totalCounter = 0
    imageCounter = 0
    for c in columns:
        counter = 0
        for d in folderDicts:
            counter = counter + int(d[c])
            imageCounter = imageCounter + 1
        totalCounter = totalCounter + counter
        lastRowSummary[c] = counter

    print imageCounter
    lastRowSummary['Annotated Images'] = allImages
    lastRowSummary['Total Annotations'] = totalCounter
    lastRowSummary['filePath'] = 'Total Annotations'
    folderDicts.append(lastRowSummary)

    with open(CSVFILENAME + '.csv', 'w') as csvfile:
        fieldnames = folderDicts[0].keys()
        myorder = ['filePath']
        allClasses.sort()
        for c in allClasses:
            myorder.append(c)
        myorder.append('Total Annotations')
        myorder.append('Annotated Images')

        filewriter = csv.DictWriter(csvfile, fieldnames=myorder)
        filewriter.writeheader()

        for ww in folderDicts:
            filewriter.writerow(ww)
