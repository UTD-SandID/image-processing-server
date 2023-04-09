#!/usr/bin/env python
# coding: utf-8

# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
import math
import os
from rembg import remove
from PIL import Image
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from matplotlib import pyplot as plt

def midpoint(pointA, pointB):
    return ((pointA[0] + pointB[0]) * 0.5, (pointA[1] + pointB[1]) * 0.5)

def rmbgJPG(path):
    input_path = path
    input = Image.open(input_path)
    output = remove(input)
    rgb_im = output.convert('RGB')
    rgb_im.save("result.jpg")
    return "result.jpg"

def getRescaleFactor(imgPath, coinLength, coinError):
    irlLength = coinLength #diameter of physical coin
    lengthErr = coinError #margin of error in diameters of ellipse before Bad Image Error
    #path = "bwnhd.jpg"
    #path = "bao_emb.jpg"
    #path = "wao_100.jpg"
    #path = "brgr.jpg"
    path = imgPath

    img = cv2.imread(path)
    plt.ylabel("Y px ct")
    plt.title("First")
    plt.imshow(img)

    bgr = cv2.imread(rmbgJPG(path))
    #plt.imshow(bgr)

    h, w, c = bgr.shape
    maxD = max(h, w)
    #print("MaxDimension: ", maxD)
    ratio = math.ceil(maxD / 250)
    if ratio % 2 == 0:
        ratio = ratio + 1
    print("Frame Size Ratio:" , ratio)
    gr = cv2.cvtColor(bgr, cv2.COLOR_RGB2GRAY)
    #gr = cv2.GaussianBlur(gr, (ratio, ratio), 0)
    #gr = cv2.medianBlur(gr,ratio)
    #gr = cv2.blur(gr,(ratio,ratio))
    gr = cv2.bilateralFilter(gr,ratio,75,75)

    # showing image
    #plt.imshow(gr)
    #plt.ylabel("Y px ct")

    edge = cv2.Canny(gr, 50, 100, apertureSize = 7)
    #plt.imshow(edge)
    #plt.show()

    edge = cv2.dilate(edge, None, iterations=10)
    #plt.imshow(edge)
    #plt.show()

    edge = cv2.erode(edge, None, iterations=10)
    #plt.imshow(edge)
    #plt.show()

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

    # loop over the contours individually
    orig = img.copy()
    for c in cnts:
        # anything less than a 100px considered noise
        if cv2.contourArea(c) < 750:
            continue
        #print(cv2.contourArea(c))
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        # ordering points to touch max and min diameters
        box = perspective.order_points(box)
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
        print("PPM: ", pixelsPerMetric)
        if (min(dA, dB) * (1+lengthErr)) < (max(dA, dB)):
            print(dA, " | ", dB, " + ", lengthErr)
            print("Coin proportions flawed.")
            exit(0)
        else:
            print(dA, " | ", dB, " + ", lengthErr)
        # compute the size of the object
        dimA = dA / pixelsPerMetric
        print("A Dimension: ", dimA)
        dimB = dB / pixelsPerMetric
        print("A Dimension: ", dimB)
        
        # draw the object sizes on the image
        cv2.putText(orig, "{:.3f}in".format(dimA),
            (int(tltrX - 150), int(tltrY - 100)), cv2.FONT_HERSHEY_SIMPLEX, math.ceil(maxD * .0015), (255, 255, 255), ratio)
        cv2.putText(orig, "{:.3f}in".format(dimB),
            (int(trbrX + 100), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, math.ceil(maxD * .0015), (255, 255, 255), ratio)
        # show the output image
        #plt.title("Coin Test Edge")
        #plt.xlabel("X pixel scaling")
        #plt.ylabel("Y pixels scaling")
        #plt.imshow(orig)
        #plt.show()
        
        head, tail = os.path.split(path)
        print(head, " h<>t ", "tail")
        cv2.imwrite(head + tail[:-4] + "_" + str(round(pixelsPerMetric, 1)) + ".jpg",orig)
        #cv2.imwrite(head + tail[:-4] + "$" + str(round(pixelsPerMetric, 1)) + ".jpg",img)
        return pixelsPerMetric

rescaleFactor = getRescaleFactor("wao_100.jpg", .835, .04)
print(rescaleFactor)