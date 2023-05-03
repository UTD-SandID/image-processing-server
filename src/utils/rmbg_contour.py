#!/usr/bin/env python
# coding: utf-8

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import numpy as np
import argparse
import imutils
import cv2
import math
import sys
from rembg import remove

from django.conf import settings

np.set_printoptions(threshold=sys.maxsize)

def midpoint(pointA, pointB):
    return ((pointA[0] + pointB[0]) * 0.5, (pointA[1] + pointB[1]) * 0.5)

def rmbgJPG(path):
    input_path = path
    input = Image.open(input_path)
    output = remove(input)
    rgb_im = output.convert('RGB')
    img_path = settings.MEDIA_ROOT + str('/temp/result.jpg')
    rgb_im.save(img_path)
    return img_path
'''
def rmbgJPG(path):
    input_path = path
    input = Image.open(input_path)
    output = remove(input)
    rgb_im = output.convert('RGB')
    rgb_im.save("result.jpg")
    return "result.jpg"
'''

def cropBox(x, y, a, b, percent):
    newX = math.floor(x + (a*percent))
    newY = math.floor(y + (b*percent))
    newA = math.floor(a - 2*(a*percent))
    newB = math.floor(b - 2*(b*percent))
    return newX, newY, newA, newB

def whitepatch_balancing(image, from_row, from_column, 
                         row_width, column_width):
    '''
    fig, ax = plt.subplots(1,2, figsize=(10,5))
    ax[0].imshow(image)
    ax[0].add_patch(Rectangle((from_column, from_row), 
                              column_width, 
                              row_width, 
                              linewidth=3,
                              edgecolor='r', facecolor='none'));
    
    ax[0].set_title('Original image')
    '''
    #plt.imshow(image)
    #plt.show()
    image_patch = image[from_row:from_row+row_width, 
                        from_column:from_column+column_width]
    image_max = (image*1.0 / 
                 image_patch.max(axis=(0, 1))).clip(0, 1)
    #plt.imshow(image_max);
    #plt.show()
    #print(type(image_max), " | ", image_max.shape)
    #print(type(image), " | ", image.shape)
    
    image_max = image_max * 255
    image_max = image_max.astype('uint8')
    #cv2.convertScaleAbs(tempIMG, alpha=(255.0))
    cv2.imwrite("temp" + ".jpg",image_max)

def getRescaleFactor(imgPath, coinLength):
    irlLength = coinLength #diameter of physical coin
    lengthErr = .1 #margin of error in diameters of ellipse before Bad Image Error
    path = imgPath

    img = cv2.imread(path)

    h, w, c = img.shape
    if h < w:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    bgr = cv2.imread(rmbgJPG(path))

    h, w, c = bgr.shape
    if h < w:
        bgr = cv2.rotate(bgr, cv2.ROTATE_90_CLOCKWISE)

    h, w, c = bgr.shape
    maxD = max(h, w)

    ratio = math.ceil(maxD / 250)
    if ratio % 2 == 0:
        ratio = ratio + 1

    gr = cv2.cvtColor(bgr, cv2.COLOR_RGB2GRAY)
    #gr = cv2.GaussianBlur(gr, (ratio, ratio), 0)
    #gr = cv2.medianBlur(gr,ratio)
    #gr = cv2.blur(gr,(ratio,ratio))
    gr = cv2.bilateralFilter(gr,ratio,75,75)

    edge = cv2.Canny(gr, 50, 100, apertureSize = 7)
    edge = cv2.dilate(edge, None, iterations=20)
    edge = cv2.erode(edge, None, iterations=20)

        # find contours in the edge map
    cnts = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    #print(cnts)

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    avgD = 0
    scaledDimX = None
    scaledDimY = None

    coinFlag = 0
    wbContour = None

    dimA, dimB, dimC, dimD = 0,0,0,0

    # loop over the contours individually
    orig = img.copy()
    for c in cnts:
        coinFlag = coinFlag + 1
        # anything less than a 100px considered noise
        if cv2.contourArea(c) < 100:
            continue
        #print("C", coinFlag, ": ", c.shape)
        #print(c)
        #print("C.area:", cv2.contourArea(c))
        if coinFlag == 1:
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            # ordering points to touch max and min diameters
            box = perspective.order_points(box)
            #print("BOX: ", box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), ratio)
            # draw original points
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 20, (255, 255, 255), ratio+10)

            # unpack the ordered bounding box
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            # compute the midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-right and bottom-right
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
            # draw the midpoints on the image
            cv2.circle(orig, (int(tltrX), int(tltrY)), 10, (255, 0, 0), ratio)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 10, (255, 0, 0), ratio)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 10, (255, 0, 0), ratio)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 10, (255, 0, 0), ratio)
            # lines between the midpoints
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), math.ceil(maxD * .003))
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), math.ceil(maxD * .003))
            # distance between the midpoints
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            avgD = (dA + dB) / 2
            if pixelsPerMetric is None:
                #print(avgD, " <- DB | ppm ->  ", pixelsPerMetric)
                pixelsPerMetric = avgD / irlLength
            if scaledDimX is None:
                ppmDiff = 750 / pixelsPerMetric
                #print(ppmDiff)
                if ppmDiff > 1:
                    #print("Image too zoomed out / Resolution too low")
                    return 'Image too zoomed out / Resolution too low.', None
                    #exit(0)
                scaledDimX = math.ceil(w * ppmDiff)
                scaledDimY = math.ceil(h * ppmDiff)
            #print("PPM: ", pixelsPerMetric)
            if (min(dA, dB) * (1+lengthErr)) < (max(dA, dB)):
                coinFlag = 1
                return 'Coin not recognized / not parallel with camera.', None
                #exit(0)
            # compute the size of the object
            dimA = dA / pixelsPerMetric
            #print(dA, " | ", dimA)
            dimB = dB / pixelsPerMetric
            #print(dB, " | ", dimB)

            # draw the object sizes on the image
            cv2.putText(orig, "{:.3f}in".format(dimA),
                (int(tltrX - 150), int(tltrY - 100)), cv2.FONT_HERSHEY_SIMPLEX, math.ceil(maxD * .0015), (255, 255, 255), ratio)
            cv2.putText(orig, "{:.3f}in".format(dimB),
                (int(trbrX + 100), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, math.ceil(maxD * .0015), (255, 255, 255), ratio)
            # show the output image
        elif coinFlag == 2:
            x,y,w,h = cv2.boundingRect(c)
            #print("Dimensions: ", x, y, w, h)
            v,b,n,m = cropBox(x, y, w, h, .3)
            v,b,n,m = math.floor(v), math.floor(b), math.floor(n), math.floor(m)
            #print(v,b,n,m)
            dimA, dimB, dimC, dimD = v, b, n, m
            orig = cv2.rectangle(orig,(x,y),(x+w,y+h),(0,255,0),math.ceil(maxD * .003))
            orig = cv2.rectangle(orig,(v,b),(v+n,b+m),(255,0,0),math.ceil(maxD * .003))
            wbContour = c
        #plt.title("Coin Test Edge")

        #plt.imshow(orig)
        #plt.show()
        
        #frame_name = path[:-4]
        #print(orig.shape)
        #cv2.imwrite(frame_name + "_" + str(round(pixelsPerMetric, 1)) + ".jpg",orig)
        #cv2.imwrite(frame_name + "$" + str(round(pixelsPerMetric, 1)) + ".jpg",img)

    tempIMG = img
    whitepatch_balancing(img, dimB, dimA, dimD, dimC)
    dim = (scaledDimX, scaledDimY)
    #print(dim)
    tempIMG = cv2.imread("temp.jpg")
    resized = cv2.resize(tempIMG, dim, interpolation = cv2.INTER_AREA)
    #plt.imshow(resized.astype('uint8'))
    #plt.show()

    cv2.imwrite(path, resized)
    return 'Processed', path
