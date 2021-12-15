from ctypes import WinDLL
import numpy as np
import pyzbar.pyzbar as pyzbar
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours

import os
import datetime
import time

from settings import *

def detect_qr_and_print(frame, gray, cascade=QR_CASCADE):
    qrcodes = cascade.detectMultiScale(gray, 2.6213145, 4, maxSize=np.shape(gray))

    for (x, y, w, h) in qrcodes:
        roi = gray[y-PADDING:y+h+PADDING, x-PADDING:x+w+PADDING]

        try:
            qrs = pyzbar.decode(roi)
            decoded_qr = qrs[0]
            byte_data = decoded_qr.data
            text_data = byte_data.decode("UTF-8")

            top = decoded_qr.rect.top
            left = decoded_qr.rect.left

            width = decoded_qr.rect.width
            height = decoded_qr.rect.height

            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2) # raw detection
            cv.rectangle(frame, (x-PADDING, y-PADDING), (x+w+PADDING, y+h+PADDING), (127, 0, 255), 2) # padded region of interest
            cv.rectangle(frame, (x+left-PADDING, y+top-PADDING), (x+left+width-PADDING, y+top+height-PADDING), (213, 231, 76), 2) # detected qr

            cv.putText(frame, text_data, (x-PADDING+left, y-PADDING+top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            print(f"[x] {datetime.datetime.now().timestamp()} - {text_data}")

            qr_location = {
                "top_left":     (x+left-PADDING, y+top-PADDING),
                "top_right":    (x+left+width-PADDING, y+top-PADDING),
                "bottom_left":  (x+left-PADDING, y+top+height-PADDING),
                "bottom_right": (x+left+width-PADDING, y+top+height-PADDING)
            }

            return qr_location

        except: pass


def iterate_and_detect_qrs(dir_path=BG_DIR_PATH):
    for img_path in os.listdir(BG_DIR_PATH):
        img = cv.imread(os.path.join(dir_path, img_path))
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        detect_qr_and_print(img, gray)
        time.sleep(1)


def midpoint(pointA, pointB):
    return (
        (pointA[0] + pointB[0]) * 0.5,
        (pointA[1] + pointB[1]) * 0.5
    )

def calculate_distance(qr_location):
    top_left_bot_left = midpoint(qr_location["top_left"], qr_location["bottom_left"])
    top_right_bot_right = midpoint(qr_location["top_right"], qr_location["bottom_right"])
    D = dist.euclidean(top_left_bot_left, top_right_bot_right)
    ref_obj = (
        (qr_location["top_left"], qr_location["top_right"], qr_location["bottom_right"], qr_location["bottom_left"]),
        ####
    )