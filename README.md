# Utilities

Basic Utilities used to make life easier. These are centered around [Darknet YOLO](https://pjreddie.com/darknet/yolo/), though can be applied to anything your heart, or dreams, desire.


# Installation

All scripts were written for Python 2.7 running on Ubuntu 16.04. While not tested on Windows, everything should be compatable, with some slight file path changes. These are simple scripts that have not been built into packages, so therefor require no installation. 

# Usage

### annotationInfo
Script to generate metadata about your Data Set. Generates a comma delimited csv file in the current working directory. Provides information about which classes have been annotated, how many annotations are found for that class, as well as which directory they are from.

### createAnnotationFiles
Script to create a folder in each child folder called Annotations. This is used after recording data, so that there is a directory to save annotations to. If Annotations is alreay present, it is ignored and not overwritten.

### Fix2017SubLogs
When 2017 images were recorded a bug was in the file naming.
Files were named in the format: Year|DayOfYear|Hour|Minute|Second|.JPEG (Irrelevant to this issue)
Note: TX1's don't have RTC Batteries, so groundhog day... (Also Irrelevant to this issue)
ABC order for numbers though produces the following (wrong) order.

1

10

11

12

2

20

21

22


If loading images with python, images.sort() recreates this, however
images.sort(key=lambda f: int(filter(str.isdigit, f))) fixes it.

This script renames all images by padding the left digit, which fixes the issue. I.e


01

02 

10

11

This should be run so that the playback of the data is in the correct order. It may take a while.

### jpegToAVI
ajadklfj

### pascal_voc_io
Requred for Skynet. A library to write the Pascal VOC Annotation format to XML. Borrorwed from [labelImg](https://github.com/tzutalin/labelImg)

### prepareTraining
lksdj

### skynet
This is potentially as evil as it sounds.

### skynetReceiver
ladkfsj


# Get help

### Issues
* **Ask**. Send me an email.
* If there's an issue, report an issue.
