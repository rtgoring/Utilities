import csv
import os
import xml.etree.ElementTree as ET
import sys
import cv2


def parse_annotation(path, filename,full_image_path):
    """
    Function to parse XML files and return dict
      :return: Dictionary containing content counters of XMLFile
    """

    in_file = open(path + '/' + filename)
    tree = ET.parse(in_file)
    root = tree.getroot()

    path_to_read = os.path.join(full_image_path,annotation)[:-3]+'jpg'

    try:
        image = cv2.imread(path_to_read)
        cv2.imshow('a',image)
        
  

        x=0
        for obj in root.iter('object'):
            cls = obj.find('name').text
            image_output_path = os.path.join(OUTPUT_DIRECTORY, cls)
            try:
                os.mkdir(image_output_path)
            except:
                pass # Already Exists
            
            #print cls
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            output_img = image[int(b[2]):int(b[3]), int(b[0]):int(b[1])]
            cv2.imshow('b',output_img)
            cv2.imwrite( os.path.join(image_output_path,filename[:-4])+str(x)+'.jpg',output_img)
            cv2.waitKey(20)
            x+=1
    except:
        print "couldn''t open " + path_to_read + " for annotation: " + path+'/'+filename


def find_image_path(annotation):
    directory_name = annotation[:-10]
    return directory_name


if __name__ == "__main__":

    ANNOTATION_DIRECTORY = 'G:\home\goring\Documents\DataSets\RobotX\Hawaii\Annotations'
    IMAGE_DIRECTORY= 'G:\home\goring\Documents\DataSets\RobotX\Hawaii\Images'
    OUTPUT_DIRECTORY = 'G:\home\goring\Documents\DataSets\RobotX\cropped'

    all_annotations = []
    try:
        os.mkdir(OUTPUT_DIRECTORY)
    except:
        pass # Already Exists

    if os.path.isdir(ANNOTATION_DIRECTORY):
        for annot in os.listdir(ANNOTATION_DIRECTORY):
            all_annotations.append(annot)
    else:
        print 'Annotation folder does not exist'
        sys.exit(-1)

    for annotation in all_annotations:
        image_path = find_image_path(annotation)
        full_image_path = os.path.join(IMAGE_DIRECTORY, image_path)
        if os.path.exists(full_image_path):
            parse_annotation(ANNOTATION_DIRECTORY, annotation,full_image_path)
            
        else:
            print annotation + ' paired image can''t be found'
  
