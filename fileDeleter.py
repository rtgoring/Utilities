import os

"""
delete objects from txt file
"""

file_name = '/home/goring/Documents/DataSets/Sub/2017/Forward/bad_images.txt'

file_in = open(file_name, 'r')

for line in file_in:
    line = line.split('\n')[0]
    try:
        os.remove(line)
        print "Removed: " + line
    except:
        pass  # Image doesn't exist
    image_file_name = line.split('/')[-1]  # last element?
    imageFileName_no_ext = image_file_name.split('.')[0]  # no extension

    #  Remove num of char for file name with, file name extension, and period
    directory = line[:-len(imageFileName_no_ext) - len(image_file_name.split('.')[1]) - 1]
    annotation = os.path.join(directory, "Annotations", imageFileName_no_ext) + '.xml'
    try:
        os.remove(annotation)
        print "removed: " + annotation
    except:
        pass  # Annotation doesn't exist
