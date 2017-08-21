import os
import random
import math

"""
Replaces find "$(pwd)" >> ../output.txt 
"""

target_directory = '/home/goring/Documents/alex/darknet/devkit/skynet4/Annotations'
destination_file_name = 'output.txt'
target_file_type = '.xml'
FULL_PATH = 1
WRITE_FILE_EXTENSION = 1
VALIDATION_RATIO = .25  # 25% Validation 75% training

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

if len(valid_set):  # If no valid, don't make empty file
    file_writer_valid = open(os.path.join(os.path.join(target_directory, '..'), 'validation.txt'), 'w')
    for f in valid_set:
        if not WRITE_FILE_EXTENSION:
            f = f.split('.')[0]  # Remove Extension

        output_string = "%s\n" % (os.path.join(target_directory, f))
        file_writer_valid.write(output_string)

    file_writer_valid.close()

file_writer_train = open(os.path.join(os.path.join(target_directory, '..'), 'train.txt'), 'w')
for f in train_set:
    if not WRITE_FILE_EXTENSION:
        f = f.split('.')[0]  # Remove Extension

    output_string = "%s\n" % (os.path.join(target_directory, f))
    file_writer_train.write(output_string)
file_writer_train.close()

print "Full Set: %d" % (len(local_files))
print "Train: %d - %.2f%% " % (len(train_set), float(len(train_set)) / len(local_files))
print "Valid: %d - %.2f%% " % (len(valid_set), float(len(valid_set)) / len(local_files))
print "DONE!"
