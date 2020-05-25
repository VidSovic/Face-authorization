import cv2 as cv
import sys
import numpy as np
import sys
imagePath = sys.argv[1]
imagePath2 = sys.argv[2]

#Prepoznavanje obraza in nastanek nove obrezane slike samo z obrazom
image = cv.imread(imagePath)
image2 = cv.imread(imagePath2)

if image is None or image2 is None:
    print('Could not open or find the images!')
    exit(0)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)

faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

face1 = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)
face2 = faceCascade.detectMultiScale(
    gray2,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

for (x, y, w, h) in face1:
    cv.rectangle(image, (x, y), (x + w, h + y), (0, 255, 0), 2)
    crop_img = image[y:y+h, x:x+w]
    print(x,y,w,h)
    break

for (x, y, w, h) in face2:
    cv.rectangle(image2, (x, y), (x + w, h + y), (0, 255, 0), 2)
    crop_img2 = image2[y:y+h, x:x+w]
    print(x,y,w,h)
    break

#cv2.imwrite('faces_detected2.jpg', crop_img2)
#cv2.imwrite('faces_detected1.jpg', crop_img)

#Izracun histogramov in njuna primerjava
src_base = crop_img
src_test1 = crop_img2

if src_base is None or src_test1 is None:
    print('Could not open or find the images!')
    exit(0)

hsv_base = cv.cvtColor(src_base, cv.COLOR_BGR2HSV)
hsv_test1 = cv.cvtColor(src_test1, cv.COLOR_BGR2HSV)

h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]
h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges
channels = [0, 1]

hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
hist_test1 = cv.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

base_test1 = cv.compareHist(hist_base, hist_test1, 0)
print('Method: 0 ', 'Result:',base_test1)

if base_test1 > 0.5:
    print("Face is simillar")
    sys.stdout.flush()
else:
    print("Face is not simillar")
    sys.stdout.flush()
