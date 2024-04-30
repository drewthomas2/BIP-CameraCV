"""
BIP C0L0R SENSOR PROTOTYPE
DREW THOMAS
1/13/24
"""

from __future__ import print_function
import numpy as np
import cv2 as cv
import time
import serial
from picamera2 import Picamera2
from picamera.array import PiRGBArray
    
def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    #picam = Picamera2()
    #rawCapture = PiRGBArray(picam)

    while True:

        picam = Picamera2()
        rawCapture = PiRGBArray(picam)

        picam.start()
        time.sleep(1)
        img = picam.capture_array("main")

        picam.close()

        # REDUCING IMAGE RESOLUTION 
        redu_factor = 0.5
        img = cv.resize(img, None, fx = redu_factor, fy = redu_factor, interpolation = cv.INTER_AREA)
        #height, width = new_img.shape[:2]
        #print('height: ' + str(height) + ' width: ' + str(width))

        # CONVERT TO HSV
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(img)

        # MASKING
        xdim, ydim, zdim = img.shape
        h_arr = []
        for a in range(xdim):
            for b in range(ydim):
                if (s[a,b] >=100) & (v[a,b] >=100):
                    h_arr.append(h[a,b])
        
        if h_arr == []: 
            mode_h = [180]
        else:
            mode_h = 2 * mode(h_arr)
        #mode_s = m_s[0]
        #mode_v = m_v[0]
        print(mode_h[0])

        a = str(mode_h[0]) + '\n'
        ser.write(a.encode('ascii'))
        line = ser.readline().decode('utf-8').rstrip()
        print('arduino says: ' + line)
        #time.sleep(1)

#source: geeks4geeks
def mode(lst):
    freq = {}
    for i in lst:
        freq.setdefault(i, 0)
        freq[i] += 1
    hf = max(freq.values())
    hflst = []
    for i, j in freq.items():
        if j == hf:
            hflst.append(i)
    return hflst

if __name__ == "__main__":
    main()
