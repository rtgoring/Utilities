import cv2
import os
'''
Usage: Create a folder in current director with name of parentFolder
'''

video_files = []
fileDirectory = 'G:/home/goring/Documents/DataSets/RobotX/Hawaii/AVIs'
for f in os.listdir(fileDirectory):
    if f.endswith(".avi") :
        video_files.append( os.path.splitext(os.path.basename(f))[0])

video_files = sorted(video_files)

print video_files

for videoFile in video_files:
    running = True
    videoExtension = '.avi'
    print videoFile
    try: #remove spaces from file name, if any...
        os.mkdir(os.path.join(fileDirectory,videoFile.replace(" ","")))
    except:
        pass
    
    cap = cv2.VideoCapture(os.path.join(fileDirectory,videoFile+videoExtension))

    imageCount = 0
    while running:
        try:
            ret, frame = cap.read()
            cv2.imshow('frame',frame)
            cv2.imwrite(os.path.join(fileDirectory,videoFile.replace(" ",""),(videoFile.replace(" ","")+ str(imageCount).zfill(6)+'.jpg')),frame)
            imageCount +=1
            cv2.waitKey(20)
        except: # end of file            
            running = False
            cap.release()
            cv2.destroyAllWindows()
        
