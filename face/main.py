import cv2
import face_recognition
import numpy as np
import os
import time

while True:

        path = 'anh'
        tenanh = []
        classname = []
        listfoder = os.listdir(path)
        slanh = []
        for s in listfoder:
            listimage = os.listdir(f'{path}/{s}')
            slanh.append(len(listimage))
            for i in listimage:
                ci = cv2.imread(f'{path}/{s}/{i}')
                tenanh.append(ci)
                classname.append(os.path.splitext(i)[0])
        def findencode(images):
            encodelist = []
            for j in images:
                j = cv2.cvtColor(j, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(j)[0]
                encodelist.append(encode)
            return encodelist
        encodelistknown = findencode(tenanh)
        def namefolder(lc):
            for k in range(0, len(listfoder)):
                if lc <= k*slanh[k]:
                    return listfoder[k]
        cam = cv2.VideoCapture(0)
        while cam.isOpened():
                a = 0
                success, im = cam.read()
                ims = cv2.resize(im, (0, 0), None, 0.25, 0.25)
                ims = cv2.cvtColor(ims, cv2.COLOR_BGR2RGB)
                faceframe = face_recognition.face_locations(ims)
                encodeframe = face_recognition.face_encodings(ims, faceframe)
                for encodeface, faceloc in zip(encodeframe, faceframe):
                    matches = face_recognition.compare_faces(encodelistknown, encodeface)
                    facedis = face_recognition.face_distance(encodelistknown, encodeface)
                    matchindex = np.argmin(facedis)
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(im, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    if matches[matchindex]:
                        cv2.putText(im, namefolder(matchindex), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
                    else:
                        anh1 = cv2.getRectSubPix(im, (x2 - x1, y2 - y1), ((x2 + x1) / 2, (y1 + y2) / 2))
                        cv2.imshow('webcam', anh1)
                        cv2.waitKey(1)
                        x = input("nhap ten  cua ban:")
                        if x in listfoder:
                            print("ten ban da ton tai ")
                        else:
                            nh = cv2.getRectSubPix(im, (x2 - x1, y2 - y1), ((x2 + x1) / 2, (y1 + y2) / 2))
                            cv2.imshow('webcam', nh)
                            path1 = os.path.join(os.getcwd(), 'anh', x)
                            os.mkdir(path1)
                            for ix in range(0, 10):
                                anh = cv2.getRectSubPix(im, (x2 - x1, y2 - y1), ((x2 + x1) / 2, (y1 + y2) / 2))
                                cv2.imwrite(path1+'/'+"anh"+str(x)+str(ix)+".jpg", anh)
                                time.sleep(0.5)
                        a = 1
                        break
                cv2.imshow('webcam', im)
                cv2.waitKey(1)
                if a == 1:break
