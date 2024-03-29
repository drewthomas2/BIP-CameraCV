# BIP C0L0R SENSOR PROTOTYPE
# DREW THOMAS
# 1/13/24

from __future__ import print_function
import numpy as np
import cv2 as cv
import time
from picamera2 import Picamera2
from picamera.array import PiRGBArray
import smbus

FULL = 0x7FFFFFFF
ADDRESS = 0x60 # change
REG_WRITE = 0x40
bus = smbus.SMBus(1)

n = 0 # count
p = 1 # times run
while n<1:
    picam = Picamera2()
    rawCapture = PiRGBArray(picam)

    picam.start()
    time.sleep(1)
    img = picam.capture_array("main")

    picam.close()

    # REDUCING IMAGE RESOLUTION 
    #redu_factor = 1
    #new_img = cv.resize(img, None, fx = redu_factor, fy = redu_factor, interpolation = cv.INTER_AREA)
    #height, width = new_img.shape[:2]
    #print('height: ' + str(height) + ' width: ' + str(width))

    # CONVERT TO HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    m_h = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=h)
    # m_s = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=s)
    # m_v = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=v)
    mode_h = 2*m_h[0]
    #mode_s = m_s[0]
    #mode_v = m_v[0]
    s = time.ctime() + ', h: ' + str(mode_h) + ', '
    print(s)
    log = open('BIP_LOG.txt', 'a')
    log.write(s)
    log.close()

    #bus.write_i2c_block_data(ADDRESS, REG_WRITE, [int(mode_h)])
    n += 1
