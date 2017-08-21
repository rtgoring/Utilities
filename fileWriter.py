import os
import random
import math

"""
Replaces find "$(pwd)" >> ../output.txt 
"""

target_directory = '/home/goring/Documents/alex/darknet/devkit/skynet5/KITTIAnnotations'
target_file_type = '.txt'
FULL_PATH = 1
WRITE_FILE_EXTENSION = 1
VALIDATION_RATIO = .15 # 25% Validation 75% training

local_files = []
train_set = []
valid_set = []

for f in os.listdir(target_directory):  # Get all files
    if f.endswith(target_file_type):  # Checks file type
        local_files.append(f)

if not FULL_PATH:  # Overwrite variable for output
    target_directory = ''

# Size of each set
max_valid = int(math.floor(float(len(local_files)) * VALIDATION_RATIO))
max_train = int(len(local_files) - max_valid)

for f in local_files:
    if VALIDATION_RATIO:
        seed = random.random() / VALIDATION_RATIO
    else:
        seed = 0

    # Random sort with limit caps
    if seed < 1:
        if len(valid_set) < max_valid:
            valid_set.append(f)
        else:
            train_set.append(f)
    else:
        if len(train_set) < max_train:
            train_set.append(f)
        else:
            valid_set.append(f)

upTarget = target_directory[:-len(target_directory.split('/')[-1])]

if len(valid_set):  # If no valid, don't make empty file
    file_writer_valid_annot = open(os.path.join(os.path.join(target_directory, '..'), 'valid_annot.txt'), 'w')
    file_writer_valid_image = open(os.path.join(os.path.join(target_directory, '..'), 'valid_image.txt'), 'w')

    for f in valid_set:
        if not WRITE_FILE_EXTENSION:
            f = f.split('.')[0]  # Remove Extension

        output_string_annot = "%s\n" % (os.path.join(target_directory, f))
        file_writer_valid_annot.write(output_string_annot)

        output_string_image = "%s\n" % (os.path.join(upTarget, 'JPEGImages', f.split('.')[0]+'.jpeg'))
        file_writer_valid_image.write(output_string_image)

    file_writer_valid_annot.close()
    file_writer_valid_image.close()


file_writer_train_annot = open(os.path.join(os.path.join(target_directory, '..'), 'train_annot.txt'), 'w')
file_writer_train_image = open(os.path.join(os.path.join(target_directory, '..'), 'train_image.txt'), 'w')

for f in train_set:
    if not WRITE_FILE_EXTENSION:
        f = f.split('.')[0]  # Remove Extension

    output_string_annot = "%s\n" % (os.path.join(target_directory, f))
    file_writer_train_annot.write(output_string_annot)

    output_string_image = "%s\n" % (os.path.join(upTarget, 'JPEGImages', f.split('.')[0]+'.jpeg'))
    file_writer_train_image.write(output_string_image)

file_writer_train_annot.close()
file_writer_train_image.close()

print "Full Set: %d" % (len(local_files))
print "Train: %d - %.2f%% " % (len(train_set), float(len(train_set)) / len(local_files))
print "Valid: %d - %.2f%% " % (len(valid_set), float(len(valid_set)) / len(local_files))
print "DONE!"
