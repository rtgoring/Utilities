import os
import socket

import pascal_voc_io as xmlwriter

UDP_IP = "127.0.0.1"
UDP_PORT = 20020
save = 0

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

directory = "/home/goring/Documents/DataSets/Sub/2017/Forward/20042114639"
folder = directory.split('/')[-1]

if os.path.isdir(directory):
    images = []
    for a in os.listdir(directory):
        if a != 'Annotations':
            images.append(a)
images.sort(key=lambda f: int(filter(str.isdigit, f)))

previousFrame = None
while True:
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

        if left < 0:
            left = 0
        if top < 0:
            top = 0
        if bottom > 1200:
            bottom = 1200
        if right > 1920:
            right = 1920

        print ("%s %d %d %d %d %d") % (cls, left, right, top, bottom, frame)
        save = 0
        if frame != previousFrame:
            print "\n\n"
        previousFrame = frame
        if save:
            if frame != previousFrame:
                imageName = images[frame].split('.')[0]
                PVW = xmlwriter.PascalVocWriter(folder, imageName, (1200, 1920, 3),
                                                localImgPath=directory + images[frame], databaseSrc='AutoGen')
            PVW.addBndBox(left, top, right, bottom, cls)
            PVW.save(directory + "/Annotations/" + imageName + '.xml')
            previousFrame = frame
