import os
import signal
import socket
import subprocess
import sys

import pascal_voc_io as xmlwriter

UDP_IP = "127.0.0.1"
UDP_PORT = 20020
save = 1
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(1)

DATA_DIRECTORY = '/home/goring/Documents/DataSets/Sub/2017/skynet'
DARKNET_DIRECTORY = '/home/goring/Documents/alex/darknet/InItToWinIt2'

if os.path.isdir(DATA_DIRECTORY):
    videoFiles = []
    for a in os.listdir(DATA_DIRECTORY):
        if os.path.isfile(os.path.join(DATA_DIRECTORY, a)):
            if a.endswith('.avi'):
                videoFiles.append(os.path.join(DATA_DIRECTORY, a))

videoFiles.sort()

for videoFileName in videoFiles:
    running = True
    try:
        print videoFileName
        folderName = videoFileName.split('.')

        directory = folderName[0]
        print directory
        folder = directory.split('/')[-1]

        if os.path.isdir(directory):
            images = []
            for a in os.listdir(directory):
                if a != 'Annotations':
                    images.append(a)
        else:
            print 'no'
        images.sort(key=lambda f: int(filter(str.isdigit, f)))
        previousFrame = None

        command = '../darknet detector demo InItToWinIt2.data InItToWinIt2.cfg Models2/InItToWinIt2_40000.weights ' + videoFileName + '\n'
        command2 = '/home/goring/Documents/alex/darknet/InItToWinIt2/skynet.sh'

        # Inorder to change dirs and run script in one command had to do sh script... & probably would have worked..
        fileWriter = open(os.path.join(DARKNET_DIRECTORY, 'skynet' + '.sh'), 'w')
        fileWriter.write('#!/bin/bash\n')
        fileWriter.write("cd '/home/goring/Documents/alex/darknet/InItToWinIt2/'\n")
        fileWriter.write(command + "\n")
        fileWriter.close()
        os.chmod(os.path.join(DARKNET_DIRECTORY, 'skynet' + '.sh'), 0755)

        pid = subprocess.Popen([command2])  # call subprocess

        frame = 0
        while frame < len(images):
            print "True"
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            if data:
                dataGood = data.split("*")
                rD = dataGood[0].split(',')
                cls = rD[0]
                _prob = rD[1]
                left = int(int(rD[2]) * 4.615384615)  # Undo the resizing
                right = int(int(rD[3]) * 4.615384615)
                top = int(int(rD[4]) * 2.884615385)
                bottom = int(int(rD[5]) * 2.884615385)
                frame = int(rD[6]) - 1

                # Error checking. YOLO returns negative numbers
                if left < 0:
                    left = 0
                if top < 0:
                    top = 0
                if bottom > 1200:
                    bottom = 1200
                if right > 1920:
                    right = 1920

                print "%s %d %d %d %d %d" % (cls, left, right, top, bottom, frame)
                if frame != previousFrame:
                    print "\n\n"
                if save:
                    if frame != previousFrame:
                        imageName = images[frame].split('.')[0]
                        PVW = xmlwriter.PascalVocWriter(folder, imageName, (1200, 1920, 3),
                                                        localImgPath=directory + images[frame], databaseSrc='AutoGen')
                    PVW.addBndBox(left, top, right, bottom, cls)
                    PVW.save(directory + "/Annotations/" + imageName + '.xml')
                    print directory + "/Annotations/" + imageName + '.xml'
                    previousFrame = frame

        os.killpg(os.getpgid(pid.pid), signal.SIGTERM)

    except:
        print sys.exc_info()
        print 'end of folder probably'
