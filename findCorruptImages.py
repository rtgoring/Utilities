import StringIO
import numpy
import os

from PIL import Image

a = numpy.zeros(4)
directory_path = '/home/goring/Documents/DataSets/Sub/2017/Forward'
error_writer = open(os.path.join(os.path.join(directory_path), 'bad_images.txt'), 'w')

parent_directories = []
corrupt_images = []
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

    for i in images:
        try:
            with open(os.path.join(directory, i), 'rb') as img_bin:  # load as numpy to see if it breaks
                buff = StringIO.StringIO()
                buff.write(img_bin.read())
                buff.seek(0)
                temp_img = numpy.array(Image.open(buff), dtype=numpy.uint8)
        except:
            print "%s is broken" % (os.path.join(directory, i))
            corrupt_images.append(os.path.join(directory, i))
            output_string = "%s\n" % (os.path.join(directory, i))
            error_writer.write(output_string)
for i in corrupt_images:
    print i

error_writer.close()
