import numpy as np
import pyzbar.pyzbar as pyzbar
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

            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2)
            cv.rectangle(frame, (x-PADDING, y-PADDING), (x+w+PADDING, y+h+PADDING), (127, 0, 255), 2)

            cv.putText(frame, text_data, (x-PADDING+left, y-PADDING+top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            print(f"[x] {datetime.datetime.now().timestamp()} - {text_data}")

        except: pass


def iterate_and_detect_qrs(dir_path=BG_DIR_PATH):
    for img_path in os.listdir(BG_DIR_PATH):
        img = cv.imread(os.path.join(dir_path, img_path))
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        detect_qr_and_print(img, gray)
        time.sleep(1)